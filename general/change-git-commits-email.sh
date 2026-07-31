#!/usr/bin/env bash

set -euo pipefail

if ! git filter-repo --version >/dev/null 2>&1; then
    echo "Error: git-filter-repo is not installed or not available in PATH. You can install it on"
    echo "Ubuntu: sudo apt update && sudo apt install git-filter-repo"
    exit 1
fi

usage() {
    cat <<EOF
Usage:
    $(basename "$0") <number_of_commits> <new_email>

Examples:
    $(basename "$0") 5 john@example.com
    $(basename "$0") 10 jane@example.com

Description:
    Rewrites the last N commits and changes the author and
    committer email address to the specified email.

Warning:
    This rewrites Git history.
EOF
}

case "${1:-}" in
    -h|--help)
        usage
        exit 0
        ;;
esac

if [ "$#" -ne 2 ]; then
    usage
    exit 1
fi

NUM_COMMITS="$1"
NEW_EMAIL="$2"

git filter-repo --force \
    --commit-callback "
if commit.original_id in [c.original_id for c in repo.get_commits('HEAD~${NUM_COMMITS}..HEAD')]:
    commit.author_email = b'$NEW_EMAIL'
    commit.committer_email = b'$NEW_EMAIL'
"
