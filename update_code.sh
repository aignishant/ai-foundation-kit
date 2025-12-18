#!/bin/bash

# Exit on error
set -e

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "Error: Please provide a version number (e.g., 0.1.7)"
    echo "Usage: ./update_code.sh <version>"
    exit 1
fi

NEW_VERSION=$1

# Validate version format
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format X.Y.Z (e.g., 0.1.7)"
    exit 1
fi

echo "🚀 Updating code for version v$NEW_VERSION..."

# 1. Update setup.py
echo "📝 Updating setup.py..."
sed -i "s/version=\"[0-9]\+\.[0-9]\+\.[0-9]\+\"/version=\"$NEW_VERSION\"/" setup.py

# verify the change
if grep -q "version=\"$NEW_VERSION\"" setup.py; then
    echo "✅ setup.py updated to $NEW_VERSION"
else
    echo "❌ Failed to update setup.py"
    exit 1
fi

# 2. Commit changes
echo "📦 Committing changes..."
git add .
git commit -m "chore: Rename `push_code.sh` to `commit_and_push.sh` and update `.gitignore`. to v$NEW_VERSION"

# 3. Push Code Only
echo "⬆️  Pushing code to main..."
git push origin main

echo "✅ Code updated and pushed to main. Ready for tagging."
