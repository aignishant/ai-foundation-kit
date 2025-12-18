#!/bin/bash

# Script to add all changes, commit with a message, and push to remote repository.
# It prompts the user for a commit message.

# Ensure we are in the repository root
REPO_ROOT="$(git rev-parse --show-toplevel)"
if [ "$?" -ne 0 ]; then
  echo "Error: Not inside a git repository."
  exit 1
fi
cd "$REPO_ROOT"

# Prompt for commit message
read -p "Enter commit message: " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
  echo "Commit message cannot be empty."
  exit 1
fi

# Add all changes
git add .

# Commit
git commit -m "$COMMIT_MSG"
if [ "$?" -ne 0 ]; then
  echo "Commit failed."
  exit 1
fi

# Pull latest changes to avoid divergence
git pull --rebase
if [ "$?" -ne 0 ]; then
  echo "Pull/rebase failed. Resolve conflicts and retry."
  exit 1
fi

# Push to the current branch's upstream using token if provided
if [ -n "$GITHUB_TOKEN" ]; then
  git push "https://${GITHUB_TOKEN}@github.com/aignishant/ai-foundation-kit.git"
else
  git push
fi
if [ "$?" -ne 0 ]; then
  echo "Push failed."
  exit 1
fi

echo "Changes have been pushed successfully."
