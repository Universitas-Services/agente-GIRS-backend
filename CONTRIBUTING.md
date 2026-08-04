# Guía de Contribución (CONTRIBUTING.md)

¡Gracias por tu interés en contribuir a **Agente GIRS**! Queremos que el proceso de colaboración sea fácil, transparente y ordenado.

## Estándares de Commits
Este proyecto utiliza la convención de [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/). Todos los mensajes de commit deben tener la siguiente estructura:

```
<tipo>[ámbito opcional]: <descripción>

[cuerpo opcional]

[pie(s) opcional(es)]
```

**Tipos permitidos:**
- `feat`: Una nueva característica.
- `fix`: Una corrección de un error (bug).
- `docs`: Cambios exclusivos en la documentación.
- `style`: Cambios que no afectan el significado del código (espacios en blanco, formato, falta de punto y coma, etc.).
- `refactor`: Un cambio en el código que ni corrige un error ni añade una característica.
- `perf`: Un cambio de código que mejora el rendimiento.
- `test`: Añadir pruebas faltantes o corregir pruebas existentes.
- `chore`: Cambios en el proceso de compilación, herramientas auxiliares o dependencias.

## Convenciones de Ramas (Branching Model)
Usamos un modelo de ramas inspirado en **GitFlow**:
- `main` o `master`: Rama principal de producción. El código aquí siempre debe ser desplegable.
- `develop` (opcional si aplica): Rama de integración para el siguiente lanzamiento.
- `feat/nombre-de-la-caracteristica`: Ramas para nuevas funcionalidades. Se desprenden de `main` o `develop`.
- `fix/nombre-del-error`: Ramas para la corrección de errores.
- `docs/nombre-del-cambio`: Ramas para actualización de la documentación.

## Cómo hacer un Pull Request (PR)
1. **Crea un Fork** del repositorio (si aplica) o crea una rama en el repositorio original.
2. **Realiza tus cambios** y haz commits semánticos siguiendo los estándares mencionados.
3. **Pasa las pruebas locales** ejecutando `agents-cli lint` y `uv run pytest`.
4. **Sube tus cambios** (`git push origin nombre-de-la-rama`).
5. **Abre un Pull Request** hacia la rama `main` (o `develop`). Asegúrate de describir claramente qué problema resuelve tu PR.
6. Espera la **revisión de código** por parte de los mantenedores y realiza los ajustes sugeridos.
