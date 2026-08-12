# V3 — Campo realista + camiseta animada

Esta versión cambia de enfoque: NO usa muñecos 3D genéricos.

La prueba se centra en:
- campo de fútbol con perspectiva y profundidad;
- césped con franjas y textura;
- líneas, áreas, círculo central y porterías;
- estadio nocturno estilizado;
- iluminación y ambiente;
- una camiseta del Villa con volumen gráfico, tejido, luces, sombras, escudo y dorsal;
- entrada animada desde fuera de pantalla;
- rotación 3D suave;
- asentamiento en el campo;
- pequeño movimiento continuo al quedarse colocada.

## Estructura

```text
index.html
style.css
scene.js
render.js
.github/workflows/render.yml
```

## Ejecutar

Sube estos archivos a la raíz de tu repositorio y `.github/workflows/render.yml`
a la carpeta correspondiente.

Después:
GitHub → Actions → "V3 - Campo realista y camiseta animada" → Run workflow.

El resultado será el artifact:
`villa-v3-campo-camiseta`

## Objetivo

Esta NO es todavía la escena final del vídeo de resultados. Es una prueba visual
para decidir si el nuevo lenguaje gráfico —campo + camisetas animadas + cámara—
es el camino correcto.

Si se aprueba, la siguiente versión puede convertir la camiseta en un componente
reutilizable y generar automáticamente:
- titulares;
- suplentes;
- posiciones;
- dorsales;
- goles;
- tarjetas;
- lobo de victoria/empate/derrota;
- resumen aleatorio.

Los datos del acta todavía NO están conectados.
