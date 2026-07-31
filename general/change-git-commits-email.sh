#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <number_of_commits> <new_email>"
    exit 1
fi

NUM_COMMITS="$1"
NEW_EMAIL="$2"

git filter-repo \
    --commit-callback "
if commit.original_id in [c.original_id for c in repo.get_commits('HEAD~${NUM_COMMITS}..HEAD')]:
    commit.author_email = b'$NEW_EMAIL'
    commit.committer_email = b'$NEW_EMAIL'
"
