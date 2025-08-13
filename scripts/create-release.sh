#!/bin/bash

VERSION=${1:-"v1.0.0"}

echo "🚀 Creando release $VERSION..."

# Crear tag
git tag $VERSION
git push origin $VERSION

echo "✅ Tag $VERSION creado y enviado"
echo "🔄 GitHub Actions construirá automáticamente los ejecutables"
echo "📦 Los ejecutables estarán disponibles en:"
echo "   https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/releases/tag/$VERSION"