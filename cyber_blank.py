import streamlit as st
import streamlit.components.v1 as components
 
st.set_page_config(page_title="⚔ Cyber Magia RPG", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
  body, .stApp { background:#0d1117 !important; }
  .stApp > header, #MainMenu, footer, header { display:none !important; visibility:hidden; }
  .block-container { padding:0 !important; max-width:100% !important; }
  iframe { border:none !important; }
</style>
""", unsafe_allow_html=True)
 
GAME = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Cyber Magia RPG</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --cyan:#00f5ff;--magenta:#ff006e;--green:#39ff14;--gold:#ffd700;
  --dark:#0d1117;--dark2:#0f1923;--dark3:#1a2332;--dark4:#1e2d40;
  --text:#c9d1d9;--textdim:#6e8098;
}
body{background:var(--dark);color:var(--text);font-family:'Share Tech Mono',monospace;overflow:hidden;height:100vh;display:flex;flex-direction:column;}
 
/* LAYOUT */
#root{display:flex;flex-direction:column;height:100vh;max-height:100vh;}
#topbar{display:flex;align-items:center;justify-content:space-between;padding:6px 16px;background:var(--dark2);border-bottom:1px solid #1e3a5f;flex-shrink:0;}
#main{display:flex;flex:1;overflow:hidden;}
#left-panel{width:220px;flex-shrink:0;background:var(--dark2);border-right:1px solid #1e3a5f;display:flex;flex-direction:column;overflow:hidden;}
#center{flex:1;display:flex;flex-direction:column;overflow:hidden;}
#canvas-wrap{flex:1;position:relative;overflow:hidden;}
#canvas{display:block;width:100%;height:100%;}
#log-bar{height:80px;background:var(--dark2);border-top:1px solid #1e3a5f;padding:6px 12px;overflow-y:auto;flex-shrink:0;}
#right-panel{width:220px;flex-shrink:0;background:var(--dark2);border-left:1px solid #1e3a5f;display:flex;flex-direction:column;overflow:hidden;}
 
/* TOPBAR */
.tb-title{font-family:'Orbitron',sans-serif;font-size:13px;font-weight:900;color:var(--cyan);text-shadow:0 0 10px var(--cyan);}
.tb-stats{display:flex;gap:16px;align-items:center;}
.tb-stat{display:flex;flex-direction:column;align-items:center;gap:1px;}
.tb-stat-label{font-size:8px;color:var(--textdim);letter-spacing:1px;}
.tb-stat-val{font-size:13px;font-weight:700;}
.bar-wrap{width:100px;height:8px;background:#111;border-radius:2px;overflow:hidden;border:1px solid #222;}
.bar-fill{height:100%;border-radius:2px;transition:width .3s;}
.bar-hp{background:linear-gradient(90deg,#ff006e,#ff6b9d);}
.bar-mp{background:linear-gradient(90deg,#00f5ff,#a78bfa);}
.bar-xp{background:linear-gradient(90deg,#39ff14,#86efac);}
 
/* PANELS */
.panel-title{font-family:'Orbitron',sans-serif;font-size:9px;letter-spacing:3px;color:var(--cyan);padding:8px 10px 4px;border-bottom:1px solid #1e3a5f;text-shadow:0 0 8px var(--cyan)44;}
.panel-section{padding:8px 10px;border-bottom:1px solid #131c28;}
 
/* MISSION BOX - neon cyan style from PDF */
.mission-box{margin:6px 8px;border:1px solid var(--cyan);border-radius:6px;padding:8px;background:#00f5ff08;position:relative;}
.mission-box::before{content:'';position:absolute;inset:0;border-radius:6px;box-shadow:0 0 8px var(--cyan)33 inset;}
.mission-title{font-size:9px;color:var(--cyan);font-family:'Orbitron',sans-serif;letter-spacing:1px;margin-bottom:4px;}
.mission-desc{font-size:9px;color:var(--text);line-height:1.5;}
.mission-reward{font-size:9px;color:var(--gold);margin-top:4px;}
 
/* INVENTORY */
.inv-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:6px 8px;}
.inv-slot{width:100%;aspect-ratio:1;background:var(--dark3);border:1px solid #1e3a5f;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;transition:all .15s;position:relative;}
.inv-slot:hover{border-color:var(--cyan);box-shadow:0 0 6px var(--cyan)44;transform:scale(1.08);}
.inv-slot.rare{border-color:var(--magenta);box-shadow:0 0 4px var(--magenta)44;}
.inv-slot.legendary{border-color:var(--gold);box-shadow:0 0 6px var(--gold)66;}
.inv-slot .qty{position:absolute;bottom:1px;right:3px;font-size:7px;color:var(--gold);}
 
/* SKILLS */
.skill-row{display:flex;flex-direction:column;gap:4px;padding:6px 8px;}
.skill-btn{background:var(--dark3);border:1px solid #1e3a5f;border-radius:4px;padding:6px 8px;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:8px;color:var(--text);font-family:'Share Tech Mono',monospace;font-size:10px;}
.skill-btn:hover:not(:disabled){border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 8px var(--cyan)33;}
.skill-btn.magic{border-color:#a78bfa44;}
.skill-btn.magic:hover:not(:disabled){border-color:#a78bfa;color:#a78bfa;box-shadow:0 0 8px #a78bfa44;}
.skill-btn:disabled{opacity:.35;cursor:not-allowed;}
.skill-cost{font-size:8px;color:var(--cyan);margin-left:auto;}
 
/* MAP */
.map-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;padding:6px 8px;}
.map-cell{aspect-ratio:1;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:11px;border:1px solid transparent;cursor:pointer;transition:all .15s;background:var(--dark3);}
.map-cell.current{border-color:var(--cyan);box-shadow:0 0 8px var(--cyan)66;animation:pulse-cyan 1.5s infinite;}
.map-cell.visited{background:#1e2d40;border-color:#1e3a5f;}
.map-cell.locked{opacity:.25;cursor:default;}
.map-cell.boss{border-color:var(--magenta)44;}
.map-cell.boss:hover{border-color:var(--magenta);box-shadow:0 0 6px var(--magenta)44;}
.map-cell.safe{border-color:#39ff1422;}
.map-cell.safe:hover{border-color:var(--green);box-shadow:0 0 6px var(--green)44;}
@keyframes pulse-cyan{0%,100%{box-shadow:0 0 6px var(--cyan)66;}50%{box-shadow:0 0 14px var(--cyan);}}
 
/* LOG */
.log-line{font-size:9px;line-height:1.6;}
.log-line.combat{color:#ff6b9d;}
.log-line.loot{color:var(--gold);}
.log-line.system{color:var(--cyan);}
.log-line.xp{color:var(--green);}
.log-line.boss{color:var(--magenta);}
 
/* BATTLE OVERLAY */
#battle-overlay{position:absolute;inset:0;background:rgba(13,17,23,.92);display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px;backdrop-filter:blur(2px);}
#battle-overlay.active{display:flex;}
 
/* Neon PINK box (PDF: alerta/poder) */
.neon-pink-box{border:1px solid var(--magenta);border-radius:8px;padding:12px 20px;background:#ff006e0a;box-shadow:0 0 16px #ff006e33;width:420px;text-align:center;}
.neon-cyan-box{border:1px solid var(--cyan);border-radius:8px;padding:12px 20px;background:#00f5ff0a;box-shadow:0 0 12px #00f5ff22;width:420px;}
 
.enemy-name{font-family:'Orbitron',sans-serif;font-size:16px;font-weight:900;color:var(--magenta);text-shadow:0 0 12px var(--magenta);letter-spacing:3px;}
.enemy-hp-wrap{width:300px;height:14px;background:#111;border:1px solid var(--magenta)44;border-radius:3px;overflow:hidden;margin:6px auto;}
.enemy-hp-fill{height:100%;background:linear-gradient(90deg,#ff006e,#ff4499);transition:width .3s;}
.enemy-ascii{font-size:48px;filter:drop-shadow(0 0 12px var(--magenta));}
 
.battle-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;}
.battle-btn{background:var(--dark3);border:1px solid #1e3a5f;border-radius:6px;padding:8px 16px;color:var(--text);font-family:'Share Tech Mono',monospace;font-size:11px;cursor:pointer;transition:all .2s;}
.battle-btn:hover:not(:disabled){transform:translateY(-2px);}
.battle-btn.attack{border-color:var(--gold)44;}
.battle-btn.attack:hover:not(:disabled){border-color:var(--gold);color:var(--gold);box-shadow:0 0 10px var(--gold)44;}
.battle-btn.magic{border-color:#a78bfa44;}
.battle-btn.magic:hover:not(:disabled){border-color:#a78bfa;color:#a78bfa;box-shadow:0 0 10px #a78bfa44;}
.battle-btn.special{border-color:var(--cyan)44;}
.battle-btn.special:hover:not(:disabled){border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 10px var(--cyan)44;}
.battle-btn.flee{border-color:var(--textdim)44;}
.battle-btn.flee:hover:not(:disabled){border-color:var(--textdim);color:var(--textdim);}
.battle-btn:disabled{opacity:.3;cursor:not-allowed;}
 
.dmg-flash{font-family:'Orbitron',sans-serif;font-size:28px;font-weight:900;color:var(--gold);text-shadow:0 0 16px var(--gold);animation:dmg-pop .5s forwards;}
@keyframes dmg-pop{0%{transform:scale(.5);opacity:1;}100%{transform:scale(1.5) translateY(-20px);opacity:0;}}
 
/* XP popup */
.xp-popup{font-family:'Orbitron',sans-serif;font-size:18px;color:var(--green);text-shadow:0 0 12px var(--green);animation:float-up 1.5s forwards;}
@keyframes float-up{0%{opacity:1;transform:translateY(0);}100%{opacity:0;transform:translateY(-40px);}}
 
/* GAME OVER / WIN */
#endscreen{position:absolute;inset:0;background:rgba(13,17,23,.96);display:none;flex-direction:column;align-items:center;justify-content:center;gap:20px;}
#endscreen.active{display:flex;}
.end-title{font-family:'Orbitron',sans-serif;font-size:36px;font-weight:900;letter-spacing:6px;}
.end-title.win{color:var(--cyan);text-shadow:0 0 24px var(--cyan);}
.end-title.lose{color:var(--magenta);text-shadow:0 0 24px var(--magenta);}
 
/* TOOLTIP */
#tooltip{position:fixed;background:var(--dark3);border:1px solid var(--cyan);border-radius:6px;padding:6px 10px;font-size:9px;color:var(--text);pointer-events:none;z-index:999;display:none;max-width:160px;line-height:1.5;}
 
/* ACTION btn */
.action-btn{background:transparent;border:1px solid var(--cyan)66;border-radius:4px;color:var(--cyan);font-family:'Share Tech Mono',monospace;font-size:9px;padding:3px 8px;cursor:pointer;letter-spacing:1px;transition:all .15s;}
.action-btn:hover{background:var(--cyan)11;border-color:var(--cyan);box-shadow:0 0 6px var(--cyan)33;}
 
/* scrollbar */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:var(--dark2);}
::-webkit-scrollbar-thumb{background:#1e3a5f;border-radius:2px;}
</style>
</head>
<body>
<div id="root">
 
<!-- TOPBAR -->
<div id="topbar">
  <div class="tb-title">⚡ CYBER MAGIA RPG</div>
  <div class="tb-stats">
    <div class="tb-stat">
      <div class="tb-stat-label">HP</div>
      <div class="bar-wrap"><div class="bar-fill bar-hp" id="bar-hp" style="width:100%"></div></div>
      <div class="tb-stat-val" id="val-hp" style="color:#ff6b9d;font-size:10px">100/100</div>
    </div>
    <div class="tb-stat">
      <div class="tb-stat-label">MP</div>
      <div class="bar-wrap"><div class="bar-fill bar-mp" id="bar-mp" style="width:100%"></div></div>
      <div class="tb-stat-val" id="val-mp" style="color:#00f5ff;font-size:10px">60/60</div>
    </div>
    <div class="tb-stat">
      <div class="tb-stat-label">XP</div>
      <div class="bar-wrap"><div class="bar-fill bar-xp" id="bar-xp" style="width:0%"></div></div>
      <div class="tb-stat-val" id="val-xp" style="color:#39ff14;font-size:10px">0/100</div>
    </div>
    <div class="tb-stat">
      <div class="tb-stat-label">LVL</div>
      <div class="tb-stat-val" id="val-lvl" style="color:var(--gold);font-size:16px;">1</div>
    </div>
    <div class="tb-stat">
      <div class="tb-stat-label">GOLD</div>
      <div class="tb-stat-val" id="val-gold" style="color:var(--gold);font-size:13px;">💰 0</div>
    </div>
    <div class="tb-stat">
      <div class="tb-stat-label">NOME</div>
      <div class="tb-stat-val" id="val-name" style="color:var(--cyan);font-size:11px;">Mago</div>
    </div>
  </div>
  <button class="action-btn" onclick="restAtInn()">🏠 DESCANSAR</button>
</div>
 
<!-- MAIN -->
<div id="main">
 
  <!-- LEFT: missions + map -->
  <div id="left-panel">
    <div class="panel-title">▸ MISSÃO ATIVA</div>
    <div id="mission-container"></div>
    <div class="panel-title" style="margin-top:4px;">▸ MAPA DO MUNDO</div>
    <div class="map-grid" id="map-grid"></div>
    <div style="padding:4px 8px;font-size:8px;color:var(--textdim);">
      ⚡ atual &nbsp;🏚 seguro &nbsp;💀 boss &nbsp;❓ desconhecido
    </div>
  </div>
 
  <!-- CENTER: canvas + log -->
  <div id="center">
    <div id="canvas-wrap">
      <canvas id="canvas"></canvas>
 
      <!-- BATTLE OVERLAY -->
      <div id="battle-overlay">
        <div class="neon-pink-box">
          <div class="enemy-ascii" id="enemy-emoji">👾</div>
          <div class="enemy-name" id="enemy-name">INIMIGO</div>
          <div style="font-size:9px;color:var(--textdim);margin:2px 0;" id="enemy-type-label">Tipo Desconhecido</div>
          <div class="enemy-hp-wrap"><div class="enemy-hp-fill" id="enemy-hp-bar" style="width:100%"></div></div>
          <div style="font-size:10px;color:#ff6b9d;" id="enemy-hp-val">100 / 100</div>
        </div>
        <div id="dmg-area" style="height:40px;display:flex;align-items:center;justify-content:center;gap:20px;"></div>
        <div class="battle-actions" id="battle-actions">
          <button class="battle-btn attack" onclick="battleAction('attack')">⚔️ ATACAR</button>
          <button class="battle-btn magic" id="btn-fireball" onclick="battleAction('fireball')">🔥 BOLA DE FOGO<span style="font-size:8px;color:var(--cyan);margin-left:6px">15MP</span></button>
          <button class="battle-btn magic" id="btn-lightning" onclick="battleAction('lightning')">⚡ RELÂMPAGO<span style="font-size:8px;color:var(--cyan);margin-left:6px">20MP</span></button>
          <button class="battle-btn special" id="btn-drain" onclick="battleAction('drain')">🌀 DRENAR MANA<span style="font-size:8px;color:var(--cyan);margin-left:6px">10MP</span></button>
          <button class="battle-btn special" id="btn-potion" onclick="battleAction('potion')">🧪 POÇÃO</button>
          <button class="battle-btn flee" onclick="battleAction('flee')">🏃 FUGIR</button>
        </div>
        <div id="battle-status" style="font-size:9px;color:var(--textdim);height:16px;"></div>
      </div>
 
      <!-- END SCREEN -->
      <div id="endscreen">
        <div class="end-title" id="end-title">GAME OVER</div>
        <div style="font-size:12px;color:var(--textdim);" id="end-sub"></div>
        <button class="action-btn" style="padding:8px 24px;font-size:12px;" onclick="resetGame()">↺ JOGAR NOVAMENTE</button>
      </div>
    </div>
 
    <!-- LOG -->
    <div id="log-bar">
      <div id="log-content"></div>
    </div>
  </div>
 
  <!-- RIGHT: inventory + skills -->
  <div id="right-panel">
    <div class="panel-title">▸ INVENTÁRIO</div>
    <div class="inv-grid" id="inv-grid"></div>
    <div style="padding:4px 8px;font-size:8px;color:var(--textdim);" id="inv-info">Hover para ver item</div>
    <div class="panel-title" style="margin-top:4px;">▸ HABILIDADES</div>
    <div class="skill-row" id="skill-row"></div>
    <div class="panel-title" style="margin-top:4px;">▸ ATRIBUTOS</div>
    <div class="panel-section" id="attr-panel" style="font-size:9px;line-height:2;"></div>
  </div>
</div>
</div><!-- root -->
 
<div id="tooltip"></div>
 
<script>
// ============================================================
// GAME DATA
// ============================================================
const ITEMS = {
  potion:       {name:'Poção de Vida',    emoji:'🧪', rarity:'common',    desc:'Restaura 40 HP',      effect:{hp:40}},
  mana_potion:  {name:'Poção de Mana',    emoji:'💜', rarity:'common',    desc:'Restaura 30 MP',      effect:{mp:30}},
  rune_shard:   {name:'Fragmento de Runa',emoji:'💎', rarity:'rare',      desc:'+5 ATK permanente',   effect:{atk:5}},
  cyber_blade:  {name:'Lâmina Cyber',     emoji:'⚔️', rarity:'rare',      desc:'Equipa: ATK +12',     effect:{equip:'weapon',atk:12}},
  neon_staff:   {name:'Cajado Neon',      emoji:'🔮', rarity:'legendary', desc:'Equipa: ATK+8 MP+20', effect:{equip:'weapon',atk:8,mp:20}},
  circuit_robe: {name:'Manto de Circuito',emoji:'🥋', rarity:'legendary', desc:'Equipa: DEF+10 HP+20',effect:{equip:'armor',def:10,hp:20}},
  gold_coin:    {name:'Moeda de Ouro',    emoji:'🪙', rarity:'common',    desc:'Vale 10 ouro',        effect:{gold:10}},
  rune_key:     {name:'Chave de Runa',    emoji:'🗝️', rarity:'rare',      desc:'Abre portais lógicos',effect:{key:true}},
  mana_crystal: {name:'Cristal de Mana',  emoji:'🔷', rarity:'rare',      desc:'Restaura 50 MP',      effect:{mp:50}},
  tome_power:   {name:'Tomo do Poder',    emoji:'📖', rarity:'legendary', desc:'+10 ATK permanente',  effect:{atk:10}},
};
 
const ENEMIES = [
  {name:'GLITCH MENOR',    emoji:'👾', type:'Cyber-Daemon',  hp:30, atk:8,  xp:20, gold:5,  loot:['gold_coin','potion']},
  {name:'ESPECTRO NEON',   emoji:'👻', type:'Fantasma Cyber',hp:45, atk:12, xp:35, gold:8,  loot:['mana_potion','rune_shard']},
  {name:'GOLEM DE CÓDIGO', emoji:'🤖', type:'Construto',     hp:70, atk:15, xp:50, gold:12, loot:['rune_shard','cyber_blade']},
  {name:'HACKER RENEGADO', emoji:'🧙', type:'Humano Cyber',  hp:55, atk:18, xp:45, gold:15, loot:['mana_crystal','potion']},
  {name:'VÍRUS ANCIÃO',    emoji:'🦠', type:'Entidade',      hp:90, atk:22, xp:80, gold:20, loot:['neon_staff','rune_key']},
];
 
const BOSSES = [
  {name:'DAEMON LORD',       emoji:'💀', type:'Boss — Nível 1', hp:150, atk:28, xp:200, gold:50,  loot:['cyber_blade','rune_key','mana_crystal']},
  {name:'MESTRE DO CÓDIGO',  emoji:'🧿', type:'Boss — Nível 2', hp:220, atk:35, xp:350, gold:80,  loot:['neon_staff','circuit_robe','tome_power']},
  {name:'CYBER-LICH SUPREMO',emoji:'💠', type:'Boss Final',     hp:350, atk:45, xp:999, gold:200, loot:['tome_power','neon_staff','circuit_robe']},
];
 
const MISSIONS = [
  {id:'m1', title:'INICIAÇÃO',         desc:'Derrote 3 Glitch Menores no setor norte.',   goal:'kill', target:'GLITCH MENOR',    count:3, reward:{xp:60, gold:20},  done:false, progress:0},
  {id:'m2', title:'CAÇA AO ESPECTRO',  desc:'Elimine 2 Espectros Neon nos setores 2-3.',  goal:'kill', target:'ESPECTRO NEON',   count:2, reward:{xp:80, gold:30},  done:false, progress:0},
  {id:'m3', title:'PORTAL TRANCADO',   desc:'Encontre 1 Chave de Runa para abrir o portal.',goal:'item',target:'rune_key',        count:1, reward:{xp:100,gold:40},  done:false, progress:0},
  {id:'m4', title:'BOSS: DAEMON LORD', desc:'Derrote o Daemon Lord no Setor 10.',         goal:'boss', target:'DAEMON LORD',      count:1, reward:{xp:200,gold:60},  done:false, progress:0},
  {id:'m5', title:'BOSS FINAL',        desc:'Destrua o Cyber-Lich Supremo e salve o reino.',goal:'boss',target:'CYBER-LICH SUPREMO',count:1,reward:{xp:999,gold:200},done:false,progress:0},
];
 
// MAP: 5x5 grid, index 0-24
// types: 'start','safe','enemy','boss','empty'
const MAP_DEF = [
  {type:'start', emoji:'🏚',label:'Base'},        {type:'enemy',emoji:'⚔️',label:'Setor 1'},  {type:'safe', emoji:'🏚',label:'Checkpoint'}, {type:'enemy',emoji:'⚔️',label:'Setor 2'},  {type:'enemy',emoji:'⚔️',label:'Setor 3'},
  {type:'enemy',emoji:'⚔️',label:'Setor 4'},      {type:'empty',emoji:'🌫',label:'Névoa'},    {type:'enemy',emoji:'⚔️',label:'Setor 5'},   {type:'safe', emoji:'🏚',label:'Pousada'},   {type:'enemy',emoji:'⚔️',label:'Setor 6'},
  {type:'boss', emoji:'💀',label:'Daemon Lord'},   {type:'enemy',emoji:'⚔️',label:'Setor 7'}, {type:'safe', emoji:'🏚',label:'Santuário'}, {type:'enemy',emoji:'⚔️',label:'Setor 8'},  {type:'enemy',emoji:'⚔️',label:'Setor 9'},
  {type:'enemy',emoji:'⚔️',label:'Setor 10'},     {type:'empty',emoji:'🌫',label:'Névoa'},    {type:'boss', emoji:'🧿',label:'Mestre'},    {type:'enemy',emoji:'⚔️',label:'Setor 11'}, {type:'safe', emoji:'🏚',label:'Refúgio'},
  {type:'enemy',emoji:'⚔️',label:'Setor 12'},     {type:'enemy',emoji:'⚔️',label:'Setor 13'},  {type:'enemy',emoji:'⚔️',label:'Setor 14'},{type:'enemy',emoji:'⚔️',label:'Setor 15'}, {type:'boss', emoji:'💠',label:'Cyber-Lich'},
];
 
// ============================================================
// GAME STATE
// ============================================================
let G = {};
 
function freshState() {
  return {
    name: 'Mago',
    level: 1, xp: 0, xpNext: 100,
    hp: 100, maxHp: 100,
    mp: 60,  maxMp: 60,
    atk: 15, def: 5,
    gold: 0,
    pos: 0,
    visited: new Set([0]),
    inventory: {potion:2, mana_potion:1},
    equipped: {weapon: null, armor: null},
    missions: JSON.parse(JSON.stringify(MISSIONS)),
    inBattle: false,
    enemy: null,
    killCounts: {},
    totalKills: 0,
    bossesDefeated: [],
    gameOver: false,
    won: false,
  };
}
 
// ============================================================
// CANVAS BACKGROUND
// ============================================================
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let canvasW, canvasH;
let circuitLines = [];
 
function resizeCanvas() {
  const wrap = document.getElementById('canvas-wrap');
  canvasW = canvas.width  = wrap.clientWidth;
  canvasH = canvas.height = wrap.clientHeight;
  buildCircuit();
}
 
function buildCircuit() {
  circuitLines = [];
  const cols = Math.floor(canvasW / 40);
  const rows = Math.floor(canvasH / 40);
  for (let i = 0; i < 40; i++) {
    const x = Math.random() * canvasW;
    const y = Math.random() * canvasH;
    const len = 30 + Math.random() * 120;
    const dir = Math.random() > .5 ? 'h' : 'v';
    circuitLines.push({x,y,len,dir,alpha:0.04+Math.random()*0.08, pulse:Math.random()*Math.PI*2, speed:0.01+Math.random()*0.02});
  }
}
 
function drawBG() {
  // Gradient background
  const grd = ctx.createLinearGradient(0,0,canvasW,canvasH);
  grd.addColorStop(0,'#0d1117');
  grd.addColorStop(0.5,'#0f1923');
  grd.addColorStop(1,'#0d1117');
  ctx.fillStyle = grd;
  ctx.fillRect(0,0,canvasW,canvasH);
 
  // Grid dots
  ctx.fillStyle = '#1e3a5f33';
  for (let x=0; x<canvasW; x+=40) for (let y=0; y<canvasH; y+=40) {
    ctx.beginPath(); ctx.arc(x,y,1,0,Math.PI*2); ctx.fill();
  }
 
  // Circuit traces
  const t = Date.now() * 0.001;
  circuitLines.forEach(l => {
    const a = l.alpha * (0.5 + 0.5*Math.sin(t*l.speed*60 + l.pulse));
    ctx.strokeStyle = `rgba(0,245,255,${a})`;
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (l.dir==='h') { ctx.moveTo(l.x,l.y); ctx.lineTo(l.x+l.len,l.y); }
    else             { ctx.moveTo(l.x,l.y); ctx.lineTo(l.x,l.y+l.len); }
    ctx.stroke();
    // node dot
    ctx.fillStyle = `rgba(0,245,255,${a*3})`;
    ctx.beginPath(); ctx.arc(l.x,l.y,2,0,Math.PI*2); ctx.fill();
  });
 
  // Floating particles
  const pts = 25;
  for (let i=0;i<pts;i++) {
    const px = (Math.sin(t*0.3+i*1.3)*0.5+0.5)*canvasW;
    const py = (Math.cos(t*0.2+i*0.9)*0.5+0.5)*canvasH;
    const a  = 0.1+0.1*Math.sin(t+i);
    ctx.fillStyle = i%3===0 ? `rgba(255,0,110,${a})` : i%3===1 ? `rgba(0,245,255,${a})` : `rgba(57,255,20,${a})`;
    ctx.beginPath(); ctx.arc(px,py,2,0,Math.PI*2); ctx.fill();
  }
 
  // Center scene text
  if (!G.inBattle && !G.gameOver && !G.won) {
    const cell = MAP_DEF[G.pos];
    ctx.save();
    ctx.font = '72px serif';
    ctx.textAlign = 'center';
    ctx.fillText(cell.emoji || '🌫', canvasW/2, canvasH/2 - 10);
    ctx.font = "bold 14px 'Orbitron',sans-serif";
    ctx.fillStyle = '#00f5ff';
    ctx.shadowColor = '#00f5ff';
    ctx.shadowBlur = 10;
    ctx.fillText(cell.label.toUpperCase(), canvasW/2, canvasH/2 + 36);
    ctx.shadowBlur = 0;
    ctx.font = "10px 'Share Tech Mono',monospace";
    ctx.fillStyle = '#6e8098';
    ctx.fillText('Clique no mapa para explorar · Pressione ESPAÇO para interagir', canvasW/2, canvasH/2 + 56);
    ctx.restore();
  }
}
 
function loop() {
  if (canvasW && canvasH) drawBG();
  requestAnimationFrame(loop);
}
 
// ============================================================
// UI RENDERS
// ============================================================
function renderHUD() {
  const hpPct = (G.hp/G.maxHp*100).toFixed(0);
  const mpPct = (G.mp/G.maxMp*100).toFixed(0);
  const xpPct = (G.xp/G.xpNext*100).toFixed(0);
  document.getElementById('bar-hp').style.width = hpPct+'%';
  document.getElementById('bar-mp').style.width = mpPct+'%';
  document.getElementById('bar-xp').style.width = xpPct+'%';
  document.getElementById('val-hp').textContent = G.hp+'/'+G.maxHp;
  document.getElementById('val-mp').textContent = G.mp+'/'+G.maxMp;
  document.getElementById('val-xp').textContent = G.xp+'/'+G.xpNext;
  document.getElementById('val-lvl').textContent = G.level;
  document.getElementById('val-gold').textContent = '💰 '+G.gold;
  document.getElementById('val-name').textContent = G.name;
}
 
function renderMission() {
  const active = G.missions.filter(m=>!m.done);
  const cont = document.getElementById('mission-container');
  if (!active.length) { cont.innerHTML = '<div style="padding:8px;font-size:9px;color:var(--green);">✅ TODAS MISSÕES COMPLETAS!</div>'; return; }
  const m = active[0];
  const prog = m.goal==='kill'||m.goal==='boss' ? `${m.progress}/${m.count}` : m.progress>0?'✅':'❌';
  cont.innerHTML = `
    <div class="mission-box">
      <div class="mission-title">📋 ${m.title}</div>
      <div class="mission-desc">${m.desc}</div>
      <div class="mission-desc" style="color:var(--textdim);margin-top:3px;">Progresso: ${prog}</div>
      <div class="mission-reward">🏆 +${m.reward.xp}XP · 💰+${m.reward.gold}</div>
    </div>`;
  // next mission preview
  if (active.length > 1) {
    const n = active[1];
    cont.innerHTML += `<div style="padding:4px 8px;font-size:8px;color:var(--textdim);">PRÓXIMA: ${n.title}</div>`;
  }
}
 
function renderMap() {
  const grid = document.getElementById('map-grid');
  grid.innerHTML = '';
  MAP_DEF.forEach((cell, i) => {
    const div = document.createElement('div');
    div.className = 'map-cell';
    if (i === G.pos) div.classList.add('current');
    else if (G.visited.has(i)) div.classList.add('visited');
    else div.classList.add('locked');
    if (cell.type==='boss') div.classList.add('boss');
    if (cell.type==='safe' || cell.type==='start') div.classList.add('safe');
    const isAdjacent = isAdjacentCell(G.pos, i);
    if (!G.visited.has(i) && !isAdjacent) div.classList.add('locked');
    div.textContent = G.visited.has(i) || i===G.pos ? cell.emoji : (isAdjacent ? '❓' : '🔒');
    div.title = G.visited.has(i)||isAdjacent||i===G.pos ? cell.label : '?';
    if (i!==G.pos && (isAdjacent || G.visited.has(i))) {
      div.onclick = () => moveToCell(i);
    }
    grid.appendChild(div);
  });
}
 
function isAdjacentCell(from, to) {
  const cols = 5;
  const fr = Math.floor(from/cols), fc = from%cols;
  const tr = Math.floor(to/cols),   tc = to%cols;
  return Math.abs(fr-tr)<=1 && Math.abs(fc-tc)<=1 && !(fr===tr&&fc===tc);
}
 
function renderInventory() {
  const grid = document.getElementById('inv-grid');
  grid.innerHTML = '';
  const slots = 16;
  const items = Object.entries(G.inventory).filter(([,q])=>q>0);
  items.forEach(([id,qty]) => {
    const item = ITEMS[id];
    if (!item) return;
    const div = document.createElement('div');
    div.className = 'inv-slot';
    if (item.rarity==='rare') div.classList.add('rare');
    if (item.rarity==='legendary') div.classList.add('legendary');
    div.innerHTML = `${item.emoji}<span class="qty">${qty>1?'x'+qty:''}</span>`;
    div.onmouseenter = (e) => showTooltip(e, `<b>${item.name}</b><br>${item.desc}<br><span style="color:var(--textdim)">[Clique para usar]</span>`);
    div.onmouseleave = hideTooltip;
    div.onclick = () => useItem(id);
    grid.appendChild(div);
  });
  // empty slots
  for (let i=items.length;i<slots;i++) {
    const div = document.createElement('div');
    div.className = 'inv-slot';
    grid.appendChild(div);
  }
}
 
function renderSkills() {
  const row = document.getElementById('skill-row');
  const skills = [
    {id:'fireball',   emoji:'🔥', name:'Bola de Fogo',   cost:15, desc:'Dano mágico 25-40', color:'#f87171'},
    {id:'lightning',  emoji:'⚡', name:'Relâmpago',       cost:20, desc:'Dano elétrico 35-55'},
    {id:'drain',      emoji:'🌀', name:'Drenar Mana',     cost:10, desc:'Rouba MP do inimigo'},
    {id:'shield',     emoji:'🛡️', name:'Escudo Mágico',  cost:15, desc:'DEF +8 por 3 turnos'},
    {id:'heal',       emoji:'💚', name:'Cura Menor',      cost:12, desc:'Recupera 30 HP'},
  ];
  row.innerHTML = skills.map(s=>`
    <button class="skill-btn magic" onclick="castSkill('${s.id}')" title="${s.desc}">
      <span>${s.emoji}</span>
      <span>${s.name}</span>
      <span class="skill-cost">${s.cost}MP</span>
    </button>`).join('');
}
 
function renderAttrs() {
  const eq = G.equipped;
  document.getElementById('attr-panel').innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:2px;">
      <span style="color:var(--textdim)">ATK</span><span style="color:var(--gold)">${G.atk}</span>
      <span style="color:var(--textdim)">DEF</span><span style="color:var(--cyan)">${G.def}</span>
      <span style="color:var(--textdim)">LVL</span><span style="color:var(--green)">${G.level}</span>
      <span style="color:var(--textdim)">KILLS</span><span style="color:#ff6b9d">${G.totalKills}</span>
      <span style="color:var(--textdim)">ARMA</span><span style="color:#a78bfa">${eq.weapon ? ITEMS[eq.weapon]?.emoji+' '+ITEMS[eq.weapon]?.name.split(' ')[0] : '—'}</span>
      <span style="color:var(--textdim)">ARMAD</span><span style="color:#a78bfa">${eq.armor  ? ITEMS[eq.armor]?.emoji+' '+ITEMS[eq.armor]?.name.split(' ')[0]  : '—'}</span>
    </div>`;
}
 
function renderAll() {
  renderHUD(); renderMission(); renderMap();
  renderInventory(); renderSkills(); renderAttrs();
}
 
// ============================================================
// LOG
// ============================================================
function log(msg, type='system') {
  const d = document.getElementById('log-content');
  const line = document.createElement('div');
  line.className = 'log-line '+type;
  const time = new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  line.textContent = `[${time}] ${msg}`;
  d.prepend(line);
  while(d.children.length > 60) d.removeChild(d.lastChild);
}
 
// ============================================================
// MOVEMENT & EXPLORATION
// ============================================================
function moveToCell(idx) {
  if (G.inBattle || G.gameOver || G.won) return;
  if (!isAdjacentCell(G.pos, idx) && !G.visited.has(idx)) return;
  G.pos = idx;
  G.visited.add(idx);
  const cell = MAP_DEF[idx];
  log(`Você chegou em: ${cell.label}`, 'system');
  renderMap();
 
  if (cell.type === 'safe' || cell.type === 'start') {
    log('Área segura. Você recuperou alguma energia.', 'system');
    G.hp = Math.min(G.maxHp, G.hp + 20);
    G.mp = Math.min(G.maxMp, G.mp + 15);
    renderHUD();
    return;
  }
  if (cell.type === 'empty') {
    log('Névoa densa... nada aqui.', 'system');
    return;
  }
  if (cell.type === 'boss') {
    const bossIdx = [10,17,24].indexOf(idx);
    if (bossIdx >= 0 && !G.bossesDefeated.includes(idx)) {
      setTimeout(() => startBattle(BOSSES[bossIdx], true), 400);
    } else if (G.bossesDefeated.includes(idx)) {
      log('Boss já derrotado. Área limpa.', 'system');
    }
    return;
  }
  if (cell.type === 'enemy') {
    const roll = Math.random();
    if (roll > 0.35) {
      const validEnemies = ENEMIES.filter(e => {
        if (idx < 5) return ENEMIES.indexOf(e) < 2;
        if (idx < 15) return ENEMIES.indexOf(e) < 4;
        return true;
      });
      const enemy = {...validEnemies[Math.floor(Math.random()*validEnemies.length)]};
      // scale enemy to player level
      const scale = 1 + (G.level - 1) * 0.2;
      enemy.hp = Math.round(enemy.hp * scale);
      enemy.maxHp = enemy.hp;
      enemy.atk = Math.round(enemy.atk * scale);
      setTimeout(() => startBattle(enemy, false), 300);
    } else {
      log('Nenhum inimigo por aqui... por enquanto.', 'system');
      // random loot chance
      if (Math.random() < 0.3) dropRandomLoot(false);
    }
  }
}
 
function dropRandomLoot(isBoss, enemy) {
  const pool = isBoss && enemy ? enemy.loot : ['gold_coin','potion','mana_potion','rune_shard'];
  const pick = pool[Math.floor(Math.random()*pool.length)];
  if (!G.inventory[pick]) G.inventory[pick] = 0;
  G.inventory[pick]++;
  log(`💎 Item encontrado: ${ITEMS[pick]?.emoji} ${ITEMS[pick]?.name}!`, 'loot');
 
  // check mission m3 (rune_key)
  if (pick === 'rune_key') checkMissionProgress('item','rune_key');
  renderInventory();
}
 
// ============================================================
// BATTLE SYSTEM
// ============================================================
let currentEnemy = null;
let shieldTurns = 0;
 
function startBattle(enemy, isBoss) {
  currentEnemy = {...enemy, maxHp: enemy.hp};
  G.inBattle = true;
  shieldTurns = 0;
  document.getElementById('battle-overlay').classList.add('active');
  document.getElementById('enemy-emoji').textContent = enemy.emoji;
  document.getElementById('enemy-name').textContent = enemy.name;
  document.getElementById('enemy-type-label').textContent = enemy.type || '';
  updateEnemyHP();
  document.getElementById('dmg-area').innerHTML = '';
  document.getElementById('battle-status').textContent = isBoss ? '⚠ CONFRONTO COM BOSS!' : '⚔ COMBATE INICIADO!';
  if (isBoss) log(`💀 BOSS: ${enemy.name} aparece!`, 'boss');
  else log(`👾 ${enemy.name} te ataca!`, 'combat');
  updateBattleButtons();
}
 
function updateEnemyHP() {
  const e = currentEnemy;
  const pct = Math.max(0, e.hp / e.maxHp * 100);
  document.getElementById('enemy-hp-bar').style.width = pct+'%';
  document.getElementById('enemy-hp-val').textContent = Math.max(0,e.hp)+' / '+e.maxHp;
}
 
function updateBattleButtons() {
  document.getElementById('btn-fireball').disabled  = G.mp < 15;
  document.getElementById('btn-lightning').disabled = G.mp < 20;
  document.getElementById('btn-drain').disabled     = G.mp < 10;
  document.getElementById('btn-potion').disabled    = !((G.inventory['potion']||0)>0);
}
 
async function battleAction(action) {
  if (!G.inBattle) return;
  setBattleButtonsDisabled(true);
 
  let playerDmg = 0, healAmt = 0, statusMsg = '';
 
  if (action === 'flee') {
    if (Math.random() > 0.4) {
      endBattle(false, true);
      return;
    } else {
      log('Falhou ao fugir!', 'combat');
      statusMsg = 'Não conseguiu fugir!';
    }
  } else if (action === 'attack') {
    playerDmg = Math.round(G.atk * (0.8 + Math.random() * 0.6));
    const isCrit = Math.random() < 0.15;
    if (isCrit) { playerDmg = Math.round(playerDmg * 1.8); statusMsg = '⚡ CRÍTICO!'; log(`Ataque crítico: ${playerDmg} dano!`, 'combat'); }
    else log(`Ataque: ${playerDmg} dano em ${currentEnemy.name}`, 'combat');
  } else if (action === 'fireball') {
    G.mp -= 15;
    playerDmg = Math.round((25 + Math.random()*15) * (1 + G.level*0.1));
    log(`🔥 Bola de Fogo: ${playerDmg} dano mágico!`, 'combat');
  } else if (action === 'lightning') {
    G.mp -= 20;
    playerDmg = Math.round((35 + Math.random()*20) * (1 + G.level*0.1));
    log(`⚡ Relâmpago: ${playerDmg} dano elétrico!`, 'combat');
  } else if (action === 'drain') {
    G.mp -= 10;
    const drained = Math.floor(5 + Math.random()*8);
    G.mp = Math.min(G.maxMp, G.mp + drained);
    playerDmg = Math.round(8 + Math.random()*10);
    log(`🌀 Drenagem: roubou ${drained}MP, causou ${playerDmg} dano.`, 'combat');
  } else if (action === 'potion') {
    healAmt = 40;
    G.hp = Math.min(G.maxHp, G.hp + healAmt);
    G.inventory['potion']--;
    if (G.inventory['potion'] <= 0) delete G.inventory['potion'];
    log(`🧪 Poção usada: +${healAmt} HP`, 'system');
    statusMsg = `+${healAmt} HP`;
    showDmgText('+'+healAmt+' HP', '#39ff14');
    renderHUD();
    renderInventory();
    // enemy still attacks
    await delay(300);
    enemyAttack();
    setBattleButtonsDisabled(false);
    updateBattleButtons();
    return;
  }
 
  // Apply player damage
  if (playerDmg > 0) {
    currentEnemy.hp -= playerDmg;
    showDmgText('-'+playerDmg, '#ffd700');
    updateEnemyHP();
  }
 
  if (statusMsg) document.getElementById('battle-status').textContent = statusMsg;
  renderHUD();
 
  await delay(350);
 
  if (currentEnemy.hp <= 0) {
    endBattle(true, false);
    return;
  }
 
  // Enemy attacks back
  enemyAttack();
  await delay(200);
  setBattleButtonsDisabled(false);
  updateBattleButtons();
}
 
function enemyAttack() {
  const def = G.def + (shieldTurns > 0 ? 8 : 0);
  if (shieldTurns > 0) shieldTurns--;
  let dmg = Math.max(1, Math.round(currentEnemy.atk * (0.7+Math.random()*0.6) - def * 0.5));
  const dodge = Math.random() < 0.1;
  if (dodge) { log('Você esquivou do ataque!', 'system'); document.getElementById('battle-status').textContent = 'Esquiva!'; return; }
  G.hp = Math.max(0, G.hp - dmg);
  log(`${currentEnemy.name} atacou: ${dmg} dano recebido!`, 'combat');
  document.getElementById('battle-status').textContent = `-${dmg} HP`;
  renderHUD();
  if (G.hp <= 0) { setTimeout(() => endBattle(false, false), 400); }
}
 
function castSkill(id) {
  if (!G.inBattle) {
    if (id==='heal') {
      if (G.mp < 12) { log('MP insuficiente!','system'); return; }
      G.mp -= 12;
      const h = 30; G.hp = Math.min(G.maxHp, G.hp+h);
      log(`💚 Cura Menor: +${h} HP`, 'system');
      renderHUD();
    } else if (id==='shield') {
      if (G.mp < 15) { log('MP insuficiente!','system'); return; }
      G.mp -= 15; shieldTurns = 3;
      log('🛡 Escudo Mágico ativado por 3 turnos!','system');
      renderHUD();
    } else { log('Use habilidades de dano em combate!','system'); }
    return;
  }
  const costMap = {fireball:15,lightning:20,drain:10,shield:15,heal:12};
  const cost = costMap[id]||0;
  if (G.mp < cost) { log('MP insuficiente!','system'); return; }
  if (id==='heal') { battleAction('potion'); return; } // reuse potion flow without consuming potion
  battleAction(id);
}
 
function endBattle(won, fled) {
  G.inBattle = false;
  document.getElementById('battle-overlay').classList.remove('active');
  const e = currentEnemy;
 
  if (fled) { log('Você fugiu do combate.','system'); return; }
 
  if (!won) {
    log('Você foi derrotado...','boss');
    showEndScreen(false);
    return;
  }
 
  // Victory
  log(`✅ ${e.name} derrotado! +${e.xp}XP +${e.gold}💰`,'xp');
  gainXP(e.xp);
  G.gold += e.gold;
  G.totalKills++;
 
  // Kill count & mission
  if (!G.killCounts[e.name]) G.killCounts[e.name] = 0;
  G.killCounts[e.name]++;
  checkMissionProgress('kill', e.name);
  const isBoss = BOSSES.some(b=>b.name===e.name);
  if (isBoss) {
    checkMissionProgress('boss', e.name);
    G.bossesDefeated.push(G.pos);
    log(`🏆 BOSS DERROTADO: ${e.name}!`,'boss');
    if (e.name === 'CYBER-LICH SUPREMO') { setTimeout(()=>showEndScreen(true), 800); return; }
  }
 
  // Loot drop
  if (e.loot && Math.random() < 0.65) dropRandomLoot(isBoss, e);
  renderAll();
}
 
function checkMissionProgress(type, target) {
  G.missions.forEach(m => {
    if (m.done) return;
    if (m.goal !== type) return;
    if (m.target.toUpperCase() !== target.toUpperCase()) return;
    m.progress++;
    if (m.progress >= m.count) {
      m.done = true;
      G.xp += m.reward.xp;
      G.gold += m.reward.gold;
      log(`🏆 MISSÃO COMPLETA: ${m.title}! +${m.reward.xp}XP +${m.reward.gold}💰`,'xp');
      showXPPopup(`+${m.reward.xp} XP`);
      checkLevelUp();
    }
    renderMission();
  });
}
 
function gainXP(amount) {
  G.xp += amount;
  showXPPopup('+'+amount+' XP');
  checkLevelUp();
  renderHUD();
}
 
function checkLevelUp() {
  while (G.xp >= G.xpNext) {
    G.xp -= G.xpNext;
    G.level++;
    G.xpNext = Math.round(G.xpNext * 1.5);
    G.maxHp += 20; G.hp = G.maxHp;
    G.maxMp += 10; G.mp = G.maxMp;
    G.atk  += 4;
    G.def  += 2;
    log(`⬆ LEVEL UP! Agora você é Nível ${G.level}! +20HP +10MP +4ATK +2DEF`,'xp');
    renderAll();
  }
}
 
// ============================================================
// ITEMS
// ============================================================
function useItem(id) {
  const item = ITEMS[id];
  if (!item || !G.inventory[id] || G.inventory[id]<=0) return;
 
  const ef = item.effect;
  if (ef.hp)   { G.hp  = Math.min(G.maxHp, G.hp + ef.hp);  log(`🧪 Usou ${item.name}: +${ef.hp} HP`,'system'); }
  if (ef.mp)   { G.mp  = Math.min(G.maxMp, G.mp + ef.mp);  log(`💜 Usou ${item.name}: +${ef.mp} MP`,'system'); }
  if (ef.gold) { G.gold += ef.gold; log(`🪙 Vendeu ${item.name}: +${ef.gold} ouro`,'loot'); }
  if (ef.atk)  { G.atk += ef.atk; log(`📖 ${item.name}: ATK +${ef.atk} permanente!`,'xp'); }
 
  if (ef.equip) {
    const slot = ef.equip;
    // unequip old
    if (G.equipped[slot]) {
      const old = ITEMS[G.equipped[slot]];
      if (old?.effect?.atk) G.atk -= old.effect.atk;
      if (old?.effect?.def) G.def -= old.effect.def;
      if (old?.effect?.hp)  { G.maxHp -= old.effect.hp; G.hp = Math.min(G.hp, G.maxHp); }
      if (old?.effect?.mp)  { G.maxMp -= old.effect.mp; G.mp = Math.min(G.mp, G.maxMp); }
    }
    G.equipped[slot] = id;
    if (ef.atk) G.atk += ef.atk;
    if (ef.def) G.def += ef.def;
    if (ef.hp)  { G.maxHp += ef.hp; G.hp = Math.min(G.hp + ef.hp, G.maxHp); }
    if (ef.mp)  { G.maxMp += ef.mp; G.mp = Math.min(G.mp + ef.mp, G.maxMp); }
    log(`⚔ Equipou: ${item.name}!`,'loot');
  }
 
  if (!ef.equip) {
    G.inventory[id]--;
    if (G.inventory[id] <= 0) delete G.inventory[id];
  }
  renderAll();
}
 
function restAtInn() {
  if (G.inBattle) { log('Não pode descansar em combate!','system'); return; }
  const cost = 10 * G.level;
  if (G.gold < cost) { log(`Precisa de ${cost} ouro para descansar.`,'system'); return; }
  G.gold -= cost;
  G.hp = G.maxHp;
  G.mp = G.maxMp;
  log(`🏠 Descansou na pousada (-${cost}💰). HP e MP restaurados completamente.`,'system');
  renderAll();
}
 
// ============================================================
// VFX
// ============================================================
function showDmgText(text, color) {
  const area = document.getElementById('dmg-area');
  const span = document.createElement('span');
  span.className = 'dmg-flash';
  span.style.color = color;
  span.style.textShadow = `0 0 12px ${color}`;
  span.textContent = text;
  area.innerHTML = '';
  area.appendChild(span);
}
 
function showXPPopup(text) {
  const wrap = document.getElementById('canvas-wrap');
  const div = document.createElement('div');
  div.className = 'xp-popup';
  div.style.cssText = `position:absolute;top:40%;left:50%;transform:translateX(-50%);pointer-events:none;z-index:10;font-family:'Orbitron',sans-serif;font-size:18px;`;
  div.textContent = text;
  wrap.appendChild(div);
  setTimeout(()=>div.remove(), 1500);
}
 
function setBattleButtonsDisabled(v) {
  document.querySelectorAll('.battle-btn').forEach(b => b.disabled = v);
}
 
function showEndScreen(won) {
  G.gameOver = !won;
  G.won = won;
  const el = document.getElementById('endscreen');
  el.classList.add('active');
  const title = document.getElementById('end-title');
  const sub   = document.getElementById('end-sub');
  if (won) {
    title.className = 'end-title win';
    title.textContent = '⚡ VITÓRIA!';
    sub.textContent = `Você derrotou o Cyber-Lich Supremo! Nível ${G.level} · ${G.totalKills} inimigos · 💰${G.gold}`;
  } else {
    title.className = 'end-title lose';
    title.textContent = 'GAME OVER';
    sub.textContent = `Derrota no Nível ${G.level} · ${G.totalKills} inimigos · 💰${G.gold}`;
  }
}
 
// ============================================================
// TOOLTIP
// ============================================================
function showTooltip(e, html) {
  const tt = document.getElementById('tooltip');
  tt.innerHTML = html;
  tt.style.display = 'block';
  tt.style.left = (e.clientX+12)+'px';
  tt.style.top  = (e.clientY+12)+'px';
}
function hideTooltip() { document.getElementById('tooltip').style.display='none'; }
 
// ============================================================
// UTILS
// ============================================================
function delay(ms) { return new Promise(r=>setTimeout(r,ms)); }
 
function resetGame() {
  document.getElementById('endscreen').classList.remove('active');
  document.getElementById('battle-overlay').classList.remove('active');
  G = freshState();
  log('Novo jogo iniciado. Bem-vindo, Mago!','system');
  renderAll();
}
 
// ============================================================
// KEYBOARD
// ============================================================
document.addEventListener('keydown', e => {
  if (e.code==='Space') {
    e.preventDefault();
    if (!G.inBattle) moveToCell(G.pos); // re-trigger current cell
  }
});
 
// ============================================================
// INIT
// ============================================================
G = freshState();
window.addEventListener('resize', resizeCanvas);
resizeCanvas();
log('Sistema Cyber Magia inicializado. Bem-vindo, Mago!','system');
log('Clique nas células adjacentes do mapa para explorar.','system');
renderAll();
loop();
</script>
</body>
</html>
"""
 
components.html(GAME, height=680, scrolling=False)
 
