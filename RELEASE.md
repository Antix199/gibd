# 🚀 Releases Automáticos

## Cómo funciona

1. **Push a main/master**: Construye ejecutables como artifacts
2. **Crear tag**: Construye y publica release automáticamente
3. **Manual**: Usar workflow_dispatch desde GitHub Actions

## Crear un release

```bash
# Método 1: Desde terminal
./scripts/create-release.sh v1.0.0

# Método 2: Manualmente
git tag v1.0.0
git push origin v1.0.0
```

## Descargas

Los ejecutables se generan automáticamente para:
- **Linux**: `GlaciarIng-linux.tar.gz`
- **macOS**: `GlaciarIng-mac.zip`
- **Windows**: `GlaciarIng-windows.zip`

## Estructura de archivos

```
releases/
├── GlaciarIng-linux.tar.gz    # Ejecutable para Linux
├── GlaciarIng-mac.zip         # Ejecutable para macOS
└── GlaciarIng-windows.zip     # Ejecutable para Windows
```