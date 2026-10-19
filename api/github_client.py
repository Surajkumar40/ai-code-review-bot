"""
GitHub integration — fetch repo file trees and file contents via PyGitHub.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

try:
    from github import Github, GithubException, Auth
    _GITHUB_AVAILABLE = True
except ImportError:
    _GITHUB_AVAILABLE = False
    logger.warning("PyGitHub not installed — GitHub features disabled")


class ReviewBotError(Exception):
    """Base exception."""


class GitHubError(ReviewBotError):
    """Raised on GitHub API failures."""


SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cpp", ".cc", ".cxx", ".h", ".hpp"}

EXTENSION_TO_LANGUAGE = {
    ".py":  "python",
    ".js":  "javascript",
    ".ts":  "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".cc":  "cpp",
    ".cxx": "cpp",
    ".h":   "cpp",
    ".hpp": "cpp",
}

MAX_FILE_SIZE_KB = int(os.getenv("MAX_FILE_SIZE_KB", "500"))


@dataclass
class RepoFile:
    """Represents a single file in a GitHub repo."""
    path: str
    name: str
    language: str
    size_kb: float
    sha: str
    download_url: str = ""
    content: Optional[str] = field(default=None, repr=False)


def _get_client() -> "Github":
    """Return authenticated or anonymous GitHub client."""
    if not _GITHUB_AVAILABLE:
        raise GitHubError("PyGitHub not installed. Run: pip install PyGitHub")
    token = os.getenv("GITHUB_TOKEN", "")
    if token:
        return Github(auth=Auth.Token(token))
    logger.warning("No GITHUB_TOKEN set — using anonymous access (60 req/hr limit)")
    return Github()


def parse_repo_url(url: str) -> tuple[str, str]:
    """
    Parse a GitHub URL into (owner, repo_name).

    Args:
        url: e.g. https://github.com/owner/repo or owner/repo

    Returns:
        Tuple of (owner, repo_name)

    Raises:
        GitHubError: If the URL cannot be parsed.
    """
    url = url.strip().rstrip("/")
    # Strip https://github.com/ prefix
    for prefix in ("https://github.com/", "http://github.com/", "github.com/"):
        if url.startswith(prefix):
            url = url[len(prefix):]
            break
    parts = url.split("/")
    if len(parts) < 2:
        raise GitHubError(
            f"Invalid GitHub URL: '{url}'. Expected format: https://github.com/owner/repo"
        )
    return parts[0], parts[1]


def get_repo_branches(repo_url: str) -> list[str]:
    """
    Fetch available branches for a repo.

    Args:
        repo_url: GitHub repository URL.

    Returns:
        List of branch names.

    Raises:
        GitHubError: On API failure.
    """
    try:
        owner, repo_name = parse_repo_url(repo_url)
        g = _get_client()
        repo = g.get_repo(f"{owner}/{repo_name}")
        branches = [b.name for b in repo.get_branches()]
        logger.info(f"Fetched {len(branches)} branches for {owner}/{repo_name}")
        return branches
    except GithubException as exc:
        raise GitHubError(f"GitHub API error: {exc.data.get('message', str(exc))}") from exc
    except Exception as exc:
        raise GitHubError(f"Unexpected error fetching branches: {exc}") from exc


def get_repo_files(repo_url: str, branch: str = "main") -> list[RepoFile]:
    """
    Walk a repo's file tree and return all supported source files.

    Args:
        repo_url: GitHub repository URL.
        branch: Branch name to use.

    Returns:
        List of RepoFile objects (content not yet fetched).

    Raises:
        GitHubError: On API failure.
    """
    try:
        owner, repo_name = parse_repo_url(repo_url)
        g = _get_client()
        repo = g.get_repo(f"{owner}/{repo_name}")

        # Try the specified branch; fall back to default branch
        try:
            tree = repo.get_git_tree(branch, recursive=True)
        except GithubException:
            default_branch = repo.default_branch
            logger.warning(f"Branch '{branch}' not found — falling back to '{default_branch}'")
            tree = repo.get_git_tree(default_branch, recursive=True)

        files: list[RepoFile] = []
        for item in tree.tree:
            if item.type != "blob":
                continue
            ext = os.path.splitext(item.path)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            size_kb = round((item.size or 0) / 1024, 1)
            if size_kb > MAX_FILE_SIZE_KB:
                logger.debug(f"Skipping {item.path} — {size_kb}KB exceeds limit")
                continue
            files.append(
                RepoFile(
                    path=item.path,
                    name=os.path.basename(item.path),
                    language=EXTENSION_TO_LANGUAGE.get(ext, "unknown"),
                    size_kb=size_kb,
                    sha=item.sha,
                )
            )

        logger.info(f"Found {len(files)} supported files in {owner}/{repo_name}")
        return sorted(files, key=lambda f: f.path)

    except GithubException as exc:
        msg = exc.data.get("message", str(exc)) if isinstance(exc.data, dict) else str(exc)
        raise GitHubError(f"GitHub API error: {msg}") from exc
    except Exception as exc:
        raise GitHubError(f"Unexpected error fetching repo files: {exc}") from exc


def fetch_file_content(repo_url: str, file_path: str, branch: str = "main") -> str:
    """
    Fetch the decoded content of a single file.

    Args:
        repo_url: GitHub repository URL.
        file_path: Path to file within the repo.
        branch: Branch to fetch from.

    Returns:
        Decoded file content as string.

    Raises:
        GitHubError: On API failure.
    """
    try:
        owner, repo_name = parse_repo_url(repo_url)
        g = _get_client()
        repo = g.get_repo(f"{owner}/{repo_name}")
        content_file = repo.get_contents(file_path, ref=branch)

        if isinstance(content_file, list):
            raise GitHubError(f"Path '{file_path}' is a directory, not a file")

        decoded = content_file.decoded_content.decode("utf-8", errors="replace")
        logger.debug(f"Fetched {file_path} ({len(decoded)} chars)")
        return decoded

    except GithubException as exc:
        msg = exc.data.get("message", str(exc)) if isinstance(exc.data, dict) else str(exc)
        raise GitHubError(f"GitHub API error fetching {file_path}: {msg}") from exc
    except Exception as exc:
        raise GitHubError(f"Error fetching {file_path}: {exc}") from exc
