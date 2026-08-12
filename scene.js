// V3: escena 2.5D. La camiseta es un elemento gráfico con volumen, luz,
// sombra y transformaciones 3D CSS. No usa muñecos 3D genéricos.
const jersey = document.getElementById("jersey");
let start = performance.now();

function idleMotion(t){
  const s=(t-start)/1000;
  if(s<4.8) return;
  const y=Math.sin((s-4.8)*1.7)*5;
  const r=Math.sin((s-4.8)*1.2)*1.1;
  jersey.style.transform=`translate3d(0,${y}px,0) rotateY(${r}deg)`;
}
function frame(t){ idleMotion(t); requestAnimationFrame(frame); }
requestAnimationFrame(frame);
