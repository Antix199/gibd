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
- **Linux**: `GIBD-linux.tar.gz`
- **macOS**: `GIBD-mac.zip`
- **Windows**: `GIBD-windows.zip`

## Estructura de archivos

```
releases/
├── GIBD-linux.tar.gz    # Ejecutable para Linux
├── GIBD-mac.zip         # Ejecutable para macOS
└── GIBD-windows.zip     # Ejecutable para Windows
```