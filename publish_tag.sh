#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "Error: Please provide a version number (e.g., 0.1.7)"
    echo "Usage: ./publish_tag.sh <version>"
    exit 1
fi

NEW_VERSION=$1

if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format X.Y.Z (e.g., 0.1.7)"
    exit 1
fi

echo "🚀 Preparing to publish tag v$NEW_VERSION..."

echo "🏷️  Creating tag v$NEW_VERSION..."
git tag -f "v$NEW_VERSION"

echo "⬆️  Pushing tag to GitHub..."
git push origin "v$NEW_VERSION"

echo "🎉 Tag v$NEW_VERSION pushed!" 
echo "🚀 This should trigger the publish workflow."
echo "🔗 Check actions here: https://github.com/aignishant/ai-common-repo/actions"
