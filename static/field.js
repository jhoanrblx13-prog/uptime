const canvas = document.getElementById("field");
const ctx = canvas.getContext("2d");
const pointer = { x: innerWidth / 2, y: innerHeight / 2, on: false };
let dots = [];
function resize() {
  canvas.width = innerWidth; canvas.height = innerHeight; dots = [];
  for (let y = 16; y < canvas.height; y += 26)
    for (let x = 16; x < canvas.width; x += 26) dots.push({ x, y, h: 0 });
}
addEventListener("resize", resize);
addEventListener("pointermove", (e) => { pointer.x = e.clientX; pointer.y = e.clientY; pointer.on = true; });
resize();
function frame() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const d of dots) {
    const dx = pointer.x - d.x, dy = pointer.y - d.y;
    const t = pointer.on ? Math.max(0, 1 - Math.hypot(dx, dy) / 170) : 0;
    d.h += (t - d.h) * 0.12;
    ctx.beginPath();
    ctx.fillStyle = `rgba(230,230,230,${0.14 + d.h * 0.7})`;
    ctx.arc(d.x, d.y, 1.1 + d.h * 2, 0, 6.3);
    ctx.fill();
  }
  requestAnimationFrame(frame);
}
frame();
