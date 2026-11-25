# Artículo Exacto

Test de oposiciones (Auxiliar Administrativo del Estado, bloque I) con la cita literal del BOE en cada respuesta.

- `q/*.txt`: preguntas (ley|artículo|pregunta|correcta|3 incorrectas|cita literal).
- `check.py`: comprueba que cada cita aparece en el texto consolidado (`arts.json`) y genera `questions.json`.
- `build.py`: genera la web estática en `site/` (variables `BASE` y `GSC`).
- Cloudflare Pages: sin comando de compilación, directorio de salida `site`.
