import streamlit as st
import streamlit.components.v1 as components
 
st.set_page_config(page_title="🥊 Street Fighter Web", layout="wide", initial_sidebar_state="collapsed")
 
st.markdown("""
<style>
    body, .stApp { background: #0d1117 !important; }
    .stApp > header { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)
 
GAME_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Street Fighter Web</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0d1117;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    min-height: 100vh;
    font-family: 'Segoe UI', system-ui, sans-serif;
    overflow: hidden;
    padding: 12px 0;
  }
 
  #title {
    color: #fff;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 10px;
    text-shadow: 0 0 20px #f59e0b, 0 0 40px #f59e0b88;
  }
 
  #hud {
    width: 720px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    gap: 12px;
  }
 
  .player-block { flex: 1; display: flex; flex-direction: column; gap: 3px; }
  .p2-block { align-items: flex-end; }
 
  .fighter-name {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #ccc;
  }
 
  .hp-wrap {
    width: 100%;
    height: 16px;
    background: #111;
    border: 1px solid #333;
    border-radius: 3px;
    overflow: hidden;
    position: relative;
  }
 
  .hp-bar {
    height: 100%;
    transition: width 0.08s;
    border-radius: 2px;
    position: relative;
  }
  .hp-bar::after {
    content: '';
    position: absolute;
    top: 2px; left: 4px; right: 4px;
    height: 4px;
    background: rgba(255,255,255,0.3);
    border-radius: 2px;
  }
 
  .hp1-bar { background: linear-gradient(90deg, #16a34a, #4ade80); }
  .hp2-bar { background: linear-gradient(270deg, #16a34a, #4ade80); }
  .hp-low  { background: linear-gradient(90deg, #dc2626, #f87171) !important; }
  .hp-mid  { background: linear-gradient(90deg, #d97706, #fbbf24) !important; }
 
  .wins-row { display: flex; gap: 5px; }
  .win-gem {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #333;
    border: 1px solid #555;
    transition: all 0.3s;
  }
  .win-gem.lit {
    background: radial-gradient(circle at 35% 35%, #fde68a, #f59e0b, #92400e);
    border-color: #f59e0b;
    box-shadow: 0 0 8px #f59e0b;
  }
 
  #timer-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 64px;
  }
  #timer-label { font-size: 9px; letter-spacing: 2px; color: #888; margin-bottom: 1px; }
  #timer-val {
    font-size: 32px;
    font-weight: 900;
    color: #fff;
    line-height: 1;
    text-shadow: 0 0 15px rgba(255,255,255,0.4);
    font-variant-numeric: tabular-nums;
  }
  #timer-val.urgent { color: #f87171; text-shadow: 0 0 15px #f8717188; }
 
  #round-info {
    font-size: 10px;
    letter-spacing: 3px;
    color: #666;
    margin-bottom: 8px;
    text-transform: uppercase;
  }
 
  #canvas-wrap {
    position: relative;
    width: 720px;
    line-height: 0;
  }
 
  #gameCanvas {
    width: 720px;
    height: 380px;
    display: block;
    border: 1px solid #222;
    border-radius: 4px;
  }
 
  #overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    pointer-events: none;
  }
 
  .overlay-card {
    background: rgba(0,0,0,0.82);
    border: 1px solid #333;
    border-radius: 10px;
    padding: 18px 40px;
    text-align: center;
    backdrop-filter: blur(4px);
  }
 
  .overlay-title {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: 4px;
    color: #f59e0b;
    text-shadow: 0 0 20px #f59e0b88;
    text-transform: uppercase;
  }
 
  .overlay-sub {
    font-size: 12px;
    color: #888;
    margin-top: 4px;
    letter-spacing: 2px;
  }
 
  #controls-row {
    width: 720px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
  }
 
  .ctrl-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid #222;
    border-radius: 6px;
    padding: 6px 12px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
 
  .ctrl-title { font-size: 9px; color: #f59e0b; letter-spacing: 2px; font-weight: 700; margin-bottom: 2px; }
  .ctrl-row { font-size: 10px; color: #888; display: flex; gap: 8px; }
  .key {
    background: #1e1e1e;
    border: 1px solid #444;
    border-bottom: 2px solid #333;
    border-radius: 3px;
    padding: 1px 5px;
    font-size: 9px;
    color: #ddd;
    font-family: monospace;
  }
 
  #start-btn {
    background: transparent;
    border: 1px solid #f59e0b;
    border-radius: 6px;
    color: #f59e0b;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    padding: 8px 24px;
    cursor: pointer;
    transition: all 0.2s;
    text-transform: uppercase;
  }
  #start-btn:hover {
    background: #f59e0b22;
    box-shadow: 0 0 16px #f59e0b44;
  }
</style>
</head>
<body>
 
<div id="title">⚔ STREET BRAWLER</div>
<div id="round-info" id="round-info">Round 1 de 3</div>
 
<div id="hud">
  <div class="player-block">
    <div class="fighter-name">RYU</div>
    <div class="hp-wrap"><div class="hp-bar hp1-bar" id="hp1" style="width:100%"></div></div>
    <div class="wins-row" id="wins1"></div>
  </div>
  <div id="timer-block">
    <div id="timer-label">TIME</div>
    <div id="timer-val">60</div>
  </div>
  <div class="player-block p2-block">
    <div class="fighter-name">KEN</div>
    <div class="hp-wrap"><div class="hp-bar hp2-bar" id="hp2" style="width:100%;float:right"></div></div>
    <div class="wins-row" id="wins2"></div>
  </div>
</div>
 
<div id="canvas-wrap">
  <canvas id="gameCanvas" width="720" height="380"></canvas>
  <div id="overlay">
    <div class="overlay-card">
      <div class="overlay-title">STREET BRAWLER</div>
      <div class="overlay-sub">Pressione iniciar para jogar</div>
    </div>
  </div>
</div>
 
<div id="controls-row">
  <div class="ctrl-box">
    <div class="ctrl-title">🔵 JOGADOR 1 — RYU</div>
    <div class="ctrl-row">
      <span><span class="key">A</span><span class="key">D</span> mover</span>
      <span><span class="key">W</span> pular</span>
      <span><span class="key">S</span> bloquear</span>
    </div>
    <div class="ctrl-row">
      <span><span class="key">F</span> soco</span>
      <span><span class="key">G</span> chute</span>
      <span><span class="key">H</span> hadouken ⚡</span>
    </div>
  </div>
 
  <button id="start-btn" onclick="startGame()">▶ INICIAR</button>
 
  <div class="ctrl-box" style="align-items:flex-end">
    <div class="ctrl-title">JOGADOR 2 — KEN 🔴</div>
    <div class="ctrl-row">
      <span><span class="key">←</span><span class="key">→</span> mover</span>
      <span><span class="key">↑</span> pular</span>
      <span><span class="key">↓</span> bloquear</span>
    </div>
    <div class="ctrl-row">
      <span><span class="key">K</span> soco</span>
      <span><span class="key">L</span> chute</span>
      <span><span class="key">;</span> shoryuken ⚡</span>
    </div>
  </div>
</div>
 
<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;
const FLOOR = H - 70;
const GRAVITY = 0.65;
const JUMP = -16;
const SPEED = 4.5;
 
let gameRunning = false, roundActive = false;
let round = 1, maxRounds = 3;
let timerVal = 60, timerInterval;
let wins = [0, 0];
let keys = {};
let p1, p2;
let particles = [];
 
// ---------- PARTICLE SYSTEM ----------
function spawnParticles(x, y, color, count = 10) {
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 1 + Math.random() * 4;
    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 2,
      life: 30 + Math.random() * 20,
      maxLife: 50,
      size: 2 + Math.random() * 4,
      color
    });
  }
}
 
function updateParticles() {
  particles = particles.filter(p => p.life > 0);
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    p.vy += 0.15;
    p.life--;
  });
}
 
function drawParticles() {
  particles.forEach(p => {
    ctx.save();
    ctx.globalAlpha = p.life / p.maxLife;
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  });
}
 
// ---------- FIGHTERS ----------
function makeFighter(x, facing, id) {
  return {
    id, x, y: FLOOR, w: 46, h: 76,
    vx: 0, vy: 0,
    hp: 100, maxHp: 100,
    facing, onGround: true,
    blocking: false,
    attackTimer: 0, attackType: null,
    hitStun: 0,
    specialCooldown: 0,
    effects: [],
    legPhase: 0,
  };
}
 
function initFighters() {
  p1 = makeFighter(110, 1, 1);
  p2 = makeFighter(610, -1, 2);
}
 
// ---------- DRAWING ----------
const BG_CACHE = document.createElement('canvas');
BG_CACHE.width = W; BG_CACHE.height = H;
 
function buildBG() {
  const bc = BG_CACHE.getContext('2d');
 
  // Sky gradient
  const sky = bc.createLinearGradient(0, 0, 0, H * 0.6);
  sky.addColorStop(0, '#0a0015');
  sky.addColorStop(0.5, '#130a2e');
  sky.addColorStop(1, '#1e0a3c');
  bc.fillStyle = sky;
  bc.fillRect(0, 0, W, H);
 
  // Stars
  bc.fillStyle = '#fff';
  for (let i = 0; i < 80; i++) {
    const sx = (i * 173 % W), sy = (i * 97 % (H * 0.55));
    const r = (i % 4 === 0) ? 1.5 : 0.8;
    bc.globalAlpha = 0.4 + (i % 5) * 0.12;
    bc.beginPath(); bc.arc(sx, sy, r, 0, Math.PI*2); bc.fill();
  }
  bc.globalAlpha = 1;
 
  // Moon
  bc.fillStyle = '#f0e6c8';
  bc.shadowColor = '#f0e6c888'; bc.shadowBlur = 30;
  bc.beginPath(); bc.arc(W - 90, 55, 30, 0, Math.PI*2); bc.fill();
  bc.fillStyle = '#130a2e';
  bc.shadowBlur = 0;
  bc.beginPath(); bc.arc(W - 78, 48, 26, 0, Math.PI*2); bc.fill();
 
  // Distant city silhouette
  bc.fillStyle = '#160830';
  const buildings = [
    [0,40,50,160],[50,40,30,140],[80,30,60,150],[140,20,40,160],
    [180,35,25,145],[205,25,55,155],[260,30,35,150],[295,15,50,165],
    [345,30,30,140],[375,35,45,145],[420,20,40,160],[460,30,35,150],
    [495,10,55,170],[550,25,40,155],[590,30,30,145],[620,35,50,145],
    [670,20,50,160]
  ];
  buildings.forEach(([bx,by,bw,bh]) => {
    bc.fillRect(bx, H*0.55 - bh, bw, bh);
  });
 
  // City windows
  bc.fillStyle = '#fde68a';
  buildings.forEach(([bx,by,bw,bh]) => {
    for (let wy = H*0.55 - bh + 8; wy < H*0.55 - 10; wy += 14) {
      for (let wx = bx + 4; wx < bx + bw - 4; wx += 10) {
        if (Math.random() > 0.4) {
          bc.globalAlpha = 0.3 + Math.random() * 0.5;
          bc.fillRect(wx, wy, 5, 6);
        }
      }
    }
  });
  bc.globalAlpha = 1;
 
  // Neon sign
  bc.font = 'bold 11px monospace';
  bc.fillStyle = '#f87171';
  bc.shadowColor = '#f87171'; bc.shadowBlur = 8;
  bc.fillText('BRAWL', 310, H * 0.55 - 20);
  bc.fillStyle = '#60a5fa';
  bc.fillText('BAR', 355, H * 0.55 - 20);
  bc.shadowBlur = 0;
 
  // Ground
  const grd = bc.createLinearGradient(0, FLOOR, 0, H);
  grd.addColorStop(0, '#1c1008');
  grd.addColorStop(0.3, '#2a1a0a');
  grd.addColorStop(1, '#0d0805');
  bc.fillStyle = grd;
  bc.fillRect(0, FLOOR, W, H - FLOOR);
 
  // Floor tiles
  for (let tx = 0; tx < W; tx += 60) {
    bc.strokeStyle = '#3d2b15';
    bc.lineWidth = 1;
    bc.beginPath(); bc.moveTo(tx, FLOOR); bc.lineTo(tx, H); bc.stroke();
  }
  bc.strokeStyle = '#3d2b15';
  bc.lineWidth = 1;
  bc.beginPath(); bc.moveTo(0, FLOOR + 25); bc.lineTo(W, FLOOR + 25); bc.stroke();
 
  // Floor shine
  const shine = bc.createLinearGradient(0, FLOOR, 0, FLOOR + 20);
  shine.addColorStop(0, 'rgba(255,180,60,0.15)');
  shine.addColorStop(1, 'rgba(0,0,0,0)');
  bc.fillStyle = shine;
  bc.fillRect(0, FLOOR, W, 20);
 
  // Stage lights
  [[120, '#3b82f680'], [360, '#a855f780'], [600, '#f59e0b80']].forEach(([lx, col]) => {
    const lg = bc.createRadialGradient(lx, FLOOR, 0, lx, FLOOR, 160);
    lg.addColorStop(0, col.replace('80','22'));
    lg.addColorStop(1, 'transparent');
    bc.fillStyle = lg;
    bc.fillRect(lx - 160, FLOOR - 100, 320, 100);
  });
}
buildBG();
 
// Crowd silhouettes
function drawCrowd() {
  const heads = [
    [30,'#e74c3c'],[70,'#3498db'],[110,'#2ecc71'],[150,'#f39c12'],
    [190,'#9b59b6'],[230,'#e74c3c'],[270,'#1abc9c'],[310,'#e67e22'],
    [350,'#3498db'],[390,'#e74c3c'],[430,'#2ecc71'],[470,'#9b59b6'],
    [510,'#f39c12'],[550,'#3498db'],[590,'#e74c3c'],[630,'#2ecc71'],
    [670,'#f39c12'],[700,'#9b59b6']
  ];
  const t = Date.now() * 0.002;
  heads.forEach(([cx, col], i) => {
    const cy = H - 8 + Math.sin(t + i) * 3;
    ctx.fillStyle = col;
    ctx.globalAlpha = 0.7;
    ctx.beginPath(); ctx.arc(cx, cy - 10, 8, 0, Math.PI*2); ctx.fill();
    ctx.fillRect(cx - 7, cy - 10, 14, 14);
    // arms raised
    ctx.beginPath(); ctx.arc(cx - 12, cy - 18 + Math.sin(t*2 + i)*4, 4, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(cx + 12, cy - 18 + Math.sin(t*2 + i + 1)*4, 4, 0, Math.PI*2); ctx.fill();
    ctx.globalAlpha = 1;
  });
}
 
function drawFighter(p) {
  const x = Math.round(p.x);
  const y = Math.round(p.y);
  const f = p.facing;
 
  // Flicker on hit
  if (p.hitStun > 0 && Math.floor(Date.now() / 60) % 2 === 0) return;
 
  ctx.save();
 
  // Shadow on ground
  ctx.save();
  ctx.globalAlpha = 0.3;
  ctx.fillStyle = '#000';
  ctx.beginPath();
  ctx.ellipse(x, FLOOR, 28, 8, 0, 0, Math.PI*2);
  ctx.fill();
  ctx.restore();
 
  // Colors per player
  const isP1 = p.id === 1;
  const bodyCol   = isP1 ? '#1e3a8a' : '#7f1d1d';
  const bodyLight = isP1 ? '#3b82f6' : '#ef4444';
  const beltCol   = '#f59e0b';
  const skinCol   = '#fbbf24';
  const hairCol   = isP1 ? '#1c1917' : '#92400e';
  const gloveCol  = isP1 ? '#dc2626' : '#1d4ed8';
  const pantCol   = isP1 ? '#fff' : '#fff';
 
  ctx.translate(x, y);
 
  const bob = (p.onGround && Math.abs(p.vx) < 0.5) ? Math.sin(Date.now()*0.005) * 1.5 : 0;
  const walkCycle = p.onGround ? Math.sin(p.legPhase) : 0;
 
  // === LEGS ===
  ctx.fillStyle = pantCol;
  if (p.onGround) {
    const la = walkCycle * 12;
    // left leg
    ctx.save();
    ctx.translate(-8, -10 + bob);
    ctx.rotate((la) * Math.PI/180);
    ctx.fillRect(-6, 0, 12, 30);
    // foot
    ctx.fillStyle = '#292524';
    ctx.fillRect(-7, 28, 16, 8);
    ctx.restore();
    // right leg
    ctx.fillStyle = pantCol;
    ctx.save();
    ctx.translate(8, -10 + bob);
    ctx.rotate((-la) * Math.PI/180);
    ctx.fillRect(-6, 0, 12, 30);
    ctx.fillStyle = '#292524';
    ctx.fillRect(-7, 28, 16, 8);
    ctx.restore();
  } else {
    // airborne legs
    ctx.fillRect(-16, -20, 12, 22);
    ctx.fillRect(4, -30, 12, 22);
    ctx.fillStyle = '#292524';
    ctx.fillRect(-17, 0, 14, 8);
    ctx.fillRect(3, -10, 14, 8);
  }
 
  // === KICK EFFECT ===
  if (p.attackTimer > 0 && p.attackType === 'kick') {
    ctx.fillStyle = pantCol;
    ctx.save();
    ctx.translate(f * 10, -20 + bob);
    ctx.rotate(f * 45 * Math.PI/180);
    ctx.fillRect(-5, 0, 10, 36);
    ctx.fillStyle = '#292524';
    ctx.fillRect(-6, 33, 18, 9);
    ctx.restore();
  }
 
  // === BODY ===
  ctx.save();
  ctx.translate(0, bob);
 
  // Gi body
  ctx.fillStyle = bodyCol;
  ctx.beginPath();
  ctx.roundRect(-18, -72, 36, 44, [4, 4, 0, 0]);
  ctx.fill();
 
  // Gi collar
  ctx.fillStyle = bodyLight;
  ctx.beginPath();
  ctx.moveTo(0, -72);
  ctx.lineTo(-8, -52);
  ctx.lineTo(0, -50);
  ctx.lineTo(8, -52);
  ctx.closePath();
  ctx.fill();
 
  // Belt
  ctx.fillStyle = beltCol;
  ctx.fillRect(-18, -30, 36, 7);
  // Belt knot
  ctx.fillStyle = '#d97706';
  ctx.fillRect(-5, -31, 10, 9);
 
  // === ARMS ===
  if (p.attackTimer > 0 && p.attackType === 'punch') {
    // Punching arm
    ctx.fillStyle = bodyLight;
    ctx.fillRect(f * 12, -68, f * 38, 12);
    ctx.fillStyle = gloveCol;
    ctx.beginPath(); ctx.arc(f * (14 + 38), -62, 10, 0, Math.PI*2); ctx.fill();
    // Retracted arm
    ctx.fillStyle = bodyLight;
    ctx.fillRect(-f * 18, -65, -f * 10, 12);
    ctx.fillStyle = gloveCol;
    ctx.beginPath(); ctx.arc(-f * 26, -59, 9, 0, Math.PI*2); ctx.fill();
  } else if (p.attackTimer > 0 && p.attackType === 'special') {
    // Both hands forward
    ctx.fillStyle = bodyLight;
    ctx.fillRect(f * 8, -68, f * 44, 12);
    ctx.fillRect(f * 8, -54, f * 32, 12);
    // Energy ball glow
    const ex = f * (14 + 44), ey = -58;
    const eg = ctx.createRadialGradient(ex, ey, 0, ex, ey, 22);
    eg.addColorStop(0, isP1 ? '#bfdbfe' : '#fef3c7');
    eg.addColorStop(0.4, isP1 ? '#3b82f6' : '#f59e0b');
    eg.addColorStop(1, 'transparent');
    ctx.fillStyle = eg;
    ctx.beginPath(); ctx.arc(ex, ey, 22, 0, Math.PI*2); ctx.fill();
    // Energy ring
    ctx.strokeStyle = isP1 ? '#93c5fd' : '#fde68a';
    ctx.lineWidth = 2;
    ctx.globalAlpha = 0.8;
    ctx.beginPath(); ctx.arc(ex, ey, 26, 0, Math.PI*2); ctx.stroke();
    ctx.globalAlpha = 1;
    ctx.fillStyle = gloveCol;
    ctx.beginPath(); ctx.arc(f * 50, -62, 10, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(f * 38, -48, 10, 0, Math.PI*2); ctx.fill();
  } else {
    // Idle arms
    ctx.fillStyle = bodyLight;
    ctx.fillRect(f < 0 ? -18 : -18, -68, 10, 22);
    ctx.fillRect(f < 0 ? 8 : 8, -68, 10, 22);
    ctx.fillStyle = gloveCol;
    ctx.beginPath(); ctx.arc(-13, -47, 9, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(13, -47, 9, 0, Math.PI*2); ctx.fill();
  }
 
  // === HEAD ===
  // Neck
  ctx.fillStyle = skinCol;
  ctx.fillRect(-5, -80, 10, 12);
 
  // Head shape
  ctx.fillStyle = skinCol;
  ctx.beginPath();
  ctx.roundRect(-13, -104, 26, 28, 6);
  ctx.fill();
 
  // Hair
  ctx.fillStyle = hairCol;
  ctx.beginPath();
  ctx.roundRect(-14, -108, 28, 18, [6,6,0,0]);
  ctx.fill();
 
  // Eyes
  const eyeX1 = f * 3, eyeX2 = -f * 7;
  ctx.fillStyle = '#1c1917';
  ctx.fillRect(eyeX1, -98, 5, 5);
  ctx.fillRect(eyeX2, -98, 5, 5);
  ctx.fillStyle = '#fff';
  ctx.fillRect(eyeX1 + 1, -97, 2, 2);
  ctx.fillRect(eyeX2 + 1, -97, 2, 2);
 
  // Mouth
  ctx.strokeStyle = '#92400e';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  if (p.hitStun > 5) {
    ctx.arc(0, -88, 4, 0, Math.PI);
  } else {
    ctx.moveTo(-4, -86); ctx.lineTo(4, -86);
  }
  ctx.stroke();
 
  // Headband
  ctx.fillStyle = isP1 ? '#ef4444' : '#1d4ed8';
  ctx.fillRect(-14, -99, 28, 5);
  // Headband tail
  ctx.fillRect(f * 10, -99, f * 8, 12);
 
  ctx.restore(); // untranslate bob
 
  // Blocking shield
  if (p.blocking) {
    ctx.save();
    ctx.globalAlpha = 0.35;
    const sg = ctx.createRadialGradient(f * 20, -50, 5, f * 20, -50, 40);
    sg.addColorStop(0, '#60a5fa');
    sg.addColorStop(1, 'transparent');
    ctx.fillStyle = sg;
    ctx.beginPath(); ctx.arc(f * 20, -50, 40, 0, Math.PI*2); ctx.fill();
    ctx.globalAlpha = 0.6;
    ctx.strokeStyle = '#93c5fd';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(f * 20, -50, 35, 0, Math.PI*2); ctx.stroke();
    ctx.restore();
  }
 
  ctx.restore(); // untranslate x,y
 
  // Damage numbers
  p.effects = p.effects.filter(e => e.life > 0);
  p.effects.forEach(e => {
    ctx.save();
    ctx.globalAlpha = Math.min(1, e.life / 15);
    ctx.font = `bold ${e.size}px 'Segoe UI'`;
    ctx.textAlign = 'center';
    ctx.fillStyle = e.color;
    ctx.shadowColor = e.color;
    ctx.shadowBlur = 8;
    ctx.fillText(e.text, e.x, e.y);
    e.y -= 1.8; e.life--;
    ctx.restore();
  });
}
 
function addEffect(p, text, color, size = 18) {
  p.effects.push({ text, color, size, x: p.x, y: p.y - 110, life: 45, maxLife: 45 });
}
 
// ---------- COMBAT ----------
function getHitbox(p) {
  if (!p.attackTimer || p.attackTimer < 3) return null;
  const f = p.facing, hw = p.w / 2;
  if (p.attackType === 'punch')   return { x: p.x + f * hw, y: p.y - 68, w: f * 34, h: 18 };
  if (p.attackType === 'kick')    return { x: p.x + f * hw, y: p.y - 30, w: f * 40, h: 18 };
  if (p.attackType === 'special') return { x: p.x + f * hw, y: p.y - 70, w: f * 60, h: 28 };
  return null;
}
 
function rectsOverlap(ax, ay, aw, ah, bx, by, bw, bh) {
  const l1 = Math.min(ax, ax+aw), r1 = Math.max(ax, ax+aw);
  const l2 = Math.min(bx, bx+bw), r2 = Math.max(bx, bx+bw);
  return l1 < r2 && r1 > l2 && ay < by+bh && ay+ah > by;
}
 
function checkHits() {
  [[p1,p2],[p2,p1]].forEach(([atk, def]) => {
    if (!atk.attackTimer || atk.attackTimer < 3) return;
    const hb = getHitbox(atk);
    if (!hb) return;
    const dw = def.w, dh = def.h;
    if (rectsOverlap(hb.x, hb.y, hb.w, hb.h, def.x - dw/2, def.y - dh, dw, dh)) {
      if (def.blocking) {
        addEffect(def, 'BLOCK', '#60a5fa', 15);
        spawnParticles(def.x + def.facing * 20, def.y - 50, '#60a5fa', 6);
        atk.attackTimer = 0;
        return;
      }
      const dmgMap = { punch: 8, kick: 13, special: 24 };
      const dmg = dmgMap[atk.attackType] || 8;
      def.hp = Math.max(0, def.hp - dmg);
      def.hitStun = 15;
      def.vx = atk.facing * 5;
      atk.attackTimer = 0;
      const colMap = { punch: '#fbbf24', kick: '#f87171', special: atk.id===1?'#93c5fd':'#fde68a' };
      addEffect(def, `-${dmg}`, colMap[atk.attackType]);
      if (atk.attackType === 'special') {
        const label = atk.id === 1 ? 'HADOUKEN!' : 'SHORYUKEN!';
        addEffect(atk, label, colMap.special, 14);
      }
      const hitCol = colMap[atk.attackType];
      spawnParticles(def.x, def.y - 60, hitCol, 14);
      updateHpBars();
      if (def.hp <= 0) endRound(atk.id);
    }
  });
}
 
// ---------- PHYSICS ----------
function updateFighter(p) {
  p.vy += GRAVITY;
  p.x += p.vx;
  p.y += p.vy;
  p.vx *= 0.85;
  if (p.y >= FLOOR) { p.y = FLOOR; p.vy = 0; p.onGround = true; }
  else p.onGround = false;
  p.x = Math.max(p.w/2 + 2, Math.min(W - p.w/2 - 2, p.x));
  if (p.attackTimer > 0) p.attackTimer--;
  if (p.hitStun > 0) p.hitStun--;
  if (p.specialCooldown > 0) p.specialCooldown--;
  if (p.onGround && Math.abs(p.vx) > 0.5) p.legPhase += 0.18;
  const other = p.id === 1 ? p2 : p1;
  if (other) p.facing = (other.x > p.x) ? 1 : -1;
}
 
// ---------- INPUT ----------
function handleInput() {
  if (!roundActive) return;
  // P1
  if (keys['a']||keys['A']) { p1.vx = -SPEED; }
  else if (keys['d']||keys['D']) { p1.vx = SPEED; }
  if ((keys['w']||keys['W']) && p1.onGround) { p1.vy = JUMP; p1.onGround = false; }
  p1.blocking = !!(keys['s']||keys['S']);
  if (!p1.attackTimer && !p1.hitStun) {
    if (keys['f']||keys['F']) { p1.attackTimer=20; p1.attackType='punch'; keys['f']=keys['F']=false; }
    else if (keys['g']||keys['G']) { p1.attackTimer=24; p1.attackType='kick'; keys['g']=keys['G']=false; }
    else if ((keys['h']||keys['H']) && !p1.specialCooldown) { p1.attackTimer=30; p1.attackType='special'; p1.specialCooldown=130; keys['h']=keys['H']=false; }
  }
  // P2
  if (keys['ArrowLeft']) { p2.vx = -SPEED; }
  else if (keys['ArrowRight']) { p2.vx = SPEED; }
  if (keys['ArrowUp'] && p2.onGround) { p2.vy = JUMP; p2.onGround = false; }
  p2.blocking = !!keys['ArrowDown'];
  if (!p2.attackTimer && !p2.hitStun) {
    if (keys['k']||keys['K']) { p2.attackTimer=20; p2.attackType='punch'; keys['k']=keys['K']=false; }
    else if (keys['l']||keys['L']) { p2.attackTimer=24; p2.attackType='kick'; keys['l']=keys['L']=false; }
    else if (keys[';'] && !p2.specialCooldown) { p2.attackTimer=30; p2.attackType='special'; p2.specialCooldown=130; keys[';']=false; }
  }
}
 
// ---------- HUD ----------
function updateHpBars() {
  [p1, p2].forEach((p, i) => {
    const el = document.getElementById('hp' + (i+1));
    const pct = (p.hp / p.maxHp * 100);
    el.style.width = pct + '%';
    el.className = 'hp-bar ' + (i===0?'hp1-bar':'hp2-bar') +
      (p.hp < 30 ? ' hp-low' : p.hp < 60 ? ' hp-mid' : '');
  });
}
 
function updateWinGems() {
  [0,1].forEach(i => {
    const el = document.getElementById('wins' + (i+1));
    el.innerHTML = '';
    for (let r = 0; r < maxRounds; r++) {
      const d = document.createElement('div');
      d.className = 'win-gem' + (r < wins[i] ? ' lit' : '');
      el.appendChild(d);
    }
  });
}
 
// ---------- OVERLAY ----------
function showOverlay(title, sub) {
  document.getElementById('overlay').innerHTML =
    `<div class="overlay-card"><div class="overlay-title">${title}</div><div class="overlay-sub">${sub}</div></div>`;
}
function clearOverlay() { document.getElementById('overlay').innerHTML = ''; }
 
// ---------- ROUND LOGIC ----------
function endRound(winnerId) {
  if (!roundActive) return;
  roundActive = false;
  clearInterval(timerInterval);
  wins[winnerId - 1]++;
  updateWinGems();
  const name = winnerId === 1 ? 'RYU' : 'KEN';
  showOverlay(`🏆 ${name} VENCEU!`, 'K.O.');
  spawnParticles(p1.x, p1.y - 80, '#fbbf24', 20);
  spawnParticles(p2.x, p2.y - 80, '#fbbf24', 20);
  const needsWins = Math.ceil(maxRounds / 2);
  if (wins[winnerId-1] >= needsWins) {
    setTimeout(() => {
      showOverlay(`🎊 ${name} CAMPEÃO!`, 'Pressione novo jogo');
      document.getElementById('start-btn').textContent = '▶ NOVO JOGO';
      document.getElementById('start-btn').onclick = () => { wins=[0,0]; round=1; updateWinGems(); startRound(); };
    }, 1400);
  } else {
    round++;
    document.getElementById('round-info').textContent = `Round ${round} de ${maxRounds}`;
    setTimeout(() => {
      showOverlay('PRONTO?', 'Pressione iniciar');
      document.getElementById('start-btn').textContent = '▶ PRÓXIMO ROUND';
      document.getElementById('start-btn').onclick = startRound;
    }, 1400);
  }
}
 
function startRound() {
  clearOverlay();
  initFighters();
  updateHpBars();
  timerVal = 60;
  document.getElementById('timer-val').textContent = timerVal;
  document.getElementById('timer-val').className = '';
  clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    timerVal--;
    const el = document.getElementById('timer-val');
    el.textContent = timerVal;
    if (timerVal <= 10) el.className = 'urgent';
    if (timerVal <= 0) {
      const winner = p1.hp >= p2.hp ? 1 : 2;
      endRound(winner);
    }
  }, 1000);
  roundActive = true;
}
 
function startGame() {
  wins = [0,0]; round = 1;
  document.getElementById('round-info').textContent = `Round ${round} de ${maxRounds}`;
  document.getElementById('start-btn').textContent = '▶ INICIAR';
  document.getElementById('start-btn').onclick = startGame;
  updateWinGems();
  startRound();
  if (!gameRunning) { gameRunning = true; loop(); }
}
 
// ---------- LOOP ----------
let screenShake = 0;
function loop() {
  ctx.clearRect(0, 0, W, H);
 
  if (screenShake > 0) {
    const sx = (Math.random()-0.5)*screenShake;
    const sy = (Math.random()-0.5)*screenShake;
    ctx.save(); ctx.translate(sx, sy);
    screenShake -= 0.8;
  }
 
  ctx.drawImage(BG_CACHE, 0, 0);
  drawCrowd();
  updateParticles();
  drawParticles();
 
  if (p1 && p2) {
    if (roundActive) { handleInput(); updateFighter(p1); updateFighter(p2); checkHits(); }
    drawFighter(p1);
    drawFighter(p2);
  }
 
  if (screenShake > 0) ctx.restore();
 
  requestAnimationFrame(loop);
}
 
// Initial setup
initFighters();
updateWinGems();
loop();
 
document.addEventListener('keydown', e => {
  keys[e.key] = true;
  if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key)) e.preventDefault();
});
document.addEventListener('keyup', e => { keys[e.key] = false; });
</script>
</body>
</html>
"""
 
components.html(GAME_HTML, height=620, scrolling=False)
