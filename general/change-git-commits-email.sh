#!/usr/bin/env bash

set -euo pipefail

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

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
    echo "Error: not inside a Git repository."
    exit 1
}

git rebase -x "
CURRENT_NAME=\$(git show -s --format='%an')
CURRENT_EMAIL=\$(git show -s --format='%ae')

if [ \"\$CURRENT_EMAIL\" != \"$NEW_EMAIL\" ]; then
    git commit --amend --no-edit \
        --author=\"\$CURRENT_NAME <$NEW_EMAIL>\"
fi
" HEAD~"$NUM_COMMITS"

echo
echo "✅ Updated email address in the last $NUM_COMMITS commits."
echo
echo "Verify with:"
echo "  git log --format='%h %an <%ae>' -n $NUM_COMMITS"
echo
echo "If already pushed:"
echo "  git push --force-with-lease"
