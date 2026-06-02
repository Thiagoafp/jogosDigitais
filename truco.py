import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🃏 Truco Didático", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
  body, .stApp { background:#0a0f14 !important; }
  .stApp > header, #MainMenu, footer, header { display:none !important; visibility:hidden; }
  .block-container { padding:0 !important; max-width:100% !important; }
  iframe { border:none !important; }
</style>
""", unsafe_allow_html=True)

GAME = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --cyan:#00f5ff; --magenta:#ff006e; --green:#39ff14; --gold:#ffd700;
  --purple:#a855f7; --orange:#f97316;
  --bg:#0a0f14; --bg2:#0f1923; --bg3:#1a2332; --bg4:#1e2d40;
  --text:#c9d1d9; --dim:#6e8098;
}
body{background:var(--bg);color:var(--text);font-family:'Share Tech Mono',monospace;height:100vh;overflow:hidden;display:flex;flex-direction:column;}

/* ── LAYOUT ── */
#root{display:flex;flex-direction:column;height:100vh;}
#header{display:flex;align-items:center;justify-content:space-between;padding:10px 20px;background:var(--bg2);border-bottom:1px solid #1e3a5f;flex-shrink:0;}
#body{display:flex;flex:1;overflow:hidden;}
#code-panel{width:300px;flex-shrink:0;background:var(--bg2);border-right:1px solid #1e3a5f;overflow-y:auto;display:flex;flex-direction:column;}
#game-area{flex:1;display:flex;flex-direction:column;overflow:hidden;}
#concept-panel{width:280px;flex-shrink:0;background:var(--bg2);border-left:1px solid #1e3a5f;overflow-y:auto;}

/* ── HEADER ── */
.title{font-family:'Orbitron',sans-serif;font-size:22px;font-weight:900;color:var(--gold);text-shadow:0 0 12px var(--gold)88;letter-spacing:3px;}
.score-box{display:flex;gap:30px;}
.score-item{text-align:center;}
.score-label{font-size:13px;color:var(--dim);letter-spacing:2px;}
.score-val{font-size:28px;font-weight:700;}
.state-badge{font-family:'Orbitron',sans-serif;font-size:14px;padding:5px 14px;border-radius:3px;letter-spacing:2px;}
.state-MENU{background:#1e3a5f;color:var(--cyan);border:1px solid var(--cyan)66;}
.state-JOGANDO{background:#14532d;color:var(--green);border:1px solid var(--green)66;}
.state-TRUCO{background:#7c2d12;color:var(--orange);border:1px solid var(--orange)66;}
.state-FIM{background:#4a1d96;color:var(--purple);border:1px solid var(--purple)66;}

/* ── CODE PANEL ── */
.code-title{font-family:'Orbitron',sans-serif;font-size:13px;color:var(--cyan);padding:8px 10px 4px;border-bottom:1px solid #1e3a5f;letter-spacing:2px;}
.code-block{background:#0d1117;margin:6px 8px;border-radius:4px;padding:8px;border-left:2px solid var(--cyan);font-size:13px;line-height:1.8;}
.code-block.active-concept{border-left-color:var(--gold);background:#1a1600;animation:highlight-pulse 1s ease-in-out;}
@keyframes highlight-pulse{0%{background:#1a1600;}50%{background:#2a2400;}100%{background:#1a1600;}
}
.kw{color:var(--cyan);}     /* keyword */
.ty{color:var(--purple);}   /* type */
.st{color:#fbbf24;}         /* string */
.cm{color:var(--dim);}      /* comment */
.nm{color:var(--green);}    /* number */
.fn{color:var(--orange);}   /* function */
.op{color:var(--magenta);}  /* operator */

/* ── GAME AREA ── */
#canvas-wrap{flex:1;position:relative;}
#canvas{display:block;width:100%;height:100%;}

#game-ui{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-between;padding:14px 22px;}

/* Placar rodada */
.round-bar{display:flex;justify-content:space-between;align-items:center;}
.round-info{font-family:'Orbitron',sans-serif;font-size:18px;color:var(--gold);}
.lives-row{display:flex;gap:4px;}
.life-heart{font-size:22px;filter:drop-shadow(0 0 4px var(--magenta));}
.life-empty{font-size:22px;opacity:.2;}

/* Cartas do bot */
.bot-row{display:flex;justify-content:center;gap:12px;}
.card-back{width:80px;height:114px;background:linear-gradient(135deg,#1e3a5f,#0f1923);border:1px solid #2a4a6f;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 4px 12px #000a;}

/* Mesa de jogo */
.table-row{display:flex;justify-content:center;align-items:center;gap:36px;}
.played-slot{width:92px;height:126px;border:1px dashed #1e3a5f44;border-radius:6px;display:flex;align-items:center;justify-content:center;position:relative;}
.played-slot .slot-label{position:absolute;bottom:-20px;font-size:13px;color:var(--dim);text-align:center;width:100%;}
.card-played{width:86px;height:120px;border-radius:5px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border:1px solid #333;box-shadow:0 4px 16px #000c;font-family:'Orbitron',sans-serif;}
.card-played .c-rank{font-size:32px;font-weight:900;}
.card-played .c-suit{font-size:24px;}
.card-played.winner{box-shadow:0 0 16px var(--gold),0 4px 16px #000c;border-color:var(--gold);}

/* Cartas do jogador */
.player-row{display:flex;justify-content:center;gap:12px;}
.card-hand{width:90px;height:126px;border-radius:6px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;transition:all .2s;border:1px solid #333;font-family:'Orbitron',sans-serif;box-shadow:0 4px 12px #000a;position:relative;}
.card-hand:hover:not(.disabled){transform:translateY(-12px);box-shadow:0 12px 24px #000c,0 0 12px var(--cyan)44;border-color:var(--cyan);}
.card-hand.disabled{opacity:.4;cursor:not-allowed;pointer-events:none;}
.card-hand.played{opacity:.25;transform:translateY(4px);cursor:not-allowed;pointer-events:none;}
.card-hand .c-rank{font-size:28px;font-weight:900;}
.card-hand .c-suit{font-size:20px;}

/* Action buttons */
.action-row{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;}
.btn{background:transparent;border-radius:4px;font-family:'Share Tech Mono',monospace;font-size:16px;padding:10px 22px;cursor:pointer;transition:all .2s;letter-spacing:1px;}
.btn-green{border:1px solid var(--green)66;color:var(--green);}
.btn-green:hover:not(:disabled){background:var(--green)11;border-color:var(--green);box-shadow:0 0 8px var(--green)33;}
.btn-orange{border:1px solid var(--orange)66;color:var(--orange);}
.btn-orange:hover:not(:disabled){background:var(--orange)11;border-color:var(--orange);box-shadow:0 0 8px var(--orange)33;}
.btn-red{border:1px solid var(--magenta)66;color:var(--magenta);}
.btn-red:hover:not(:disabled){background:var(--magenta)11;border-color:var(--magenta);box-shadow:0 0 8px var(--magenta)33;}
.btn-cyan{border:1px solid var(--cyan)66;color:var(--cyan);}
.btn-cyan:hover:not(:disabled){background:var(--cyan)11;border-color:var(--cyan);box-shadow:0 0 8px var(--cyan)33;}
.btn:disabled{opacity:.3;cursor:not-allowed;}

/* Overlays */
#overlay{position:absolute;inset:0;background:rgba(10,15,20,.9);display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px;backdrop-filter:blur(3px);}
#overlay.active{display:flex;}
.ov-title{font-family:'Orbitron',sans-serif;font-size:38px;font-weight:900;letter-spacing:4px;}
.ov-sub{font-size:16px;color:var(--dim);max-width:360px;text-align:center;line-height:1.6;}
.ov-box{border-radius:8px;padding:16px 28px;text-align:center;max-width:400px;}
.ov-cyan{border:1px solid var(--cyan);background:#00f5ff08;box-shadow:0 0 20px var(--cyan)22;}
.ov-gold{border:1px solid var(--gold);background:#ffd70008;box-shadow:0 0 20px var(--gold)22;}
.ov-red{border:1px solid var(--magenta);background:#ff006e08;box-shadow:0 0 20px var(--magenta)22;}

/* Truco announcement */
#truco-announce{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:'Orbitron',sans-serif;font-size:52px;font-weight:900;color:var(--orange);text-shadow:0 0 24px var(--orange);pointer-events:none;display:none;animation:truco-pop .6s forwards;}
@keyframes truco-pop{0%{transform:translate(-50%,-50%) scale(.4);opacity:1;}60%{transform:translate(-50%,-50%) scale(1.2);}100%{transform:translate(-50%,-50%) scale(1);opacity:1;}}

/* ── CONCEPT PANEL ── */
.cpt-title{font-family:'Orbitron',sans-serif;font-size:13px;color:var(--green);padding:8px 10px 4px;border-bottom:1px solid #1e3a5f;letter-spacing:2px;}
.concept-card{margin:6px 8px;border-radius:6px;padding:10px 12px;border-left:3px solid;font-size:13px;line-height:1.7;}
.concept-card.active{animation:fade-in .4s;}
@keyframes fade-in{from{opacity:0;transform:translateX(8px);}to{opacity:1;transform:none;}}
.concept-card h4{font-size:13px;font-family:'Orbitron',sans-serif;letter-spacing:1px;margin-bottom:4px;}
.cpt-var{border-color:var(--cyan);background:#00f5ff08;}     .cpt-var h4{color:var(--cyan);}
.cpt-op{border-color:var(--gold);background:#ffd70008;}      .cpt-op h4{color:var(--gold);}
.cpt-logic{border-color:var(--purple);background:#a855f708;} .cpt-logic h4{color:var(--purple);}
.cpt-cond{border-color:var(--green);background:#39ff1408;}   .cpt-cond h4{color:var(--green);}
.cpt-loop{border-color:var(--orange);background:#f9731608;}  .cpt-loop h4{color:var(--orange);}
.cpt-event{border-color:#60a5fa;background:#60a5fa08;}       .cpt-event h4{color:#60a5fa;}
.cpt-state{border-color:var(--magenta);background:#ff006e08;}.cpt-state h4{color:var(--magenta);}
.cpt-score{border-color:#fbbf24;background:#fbbf2408;}       .cpt-score h4{color:#fbbf24;}

/* Log bar */
#log{height:70px;background:var(--bg2);border-top:1px solid #1e3a5f;padding:4px 12px;overflow-y:auto;flex-shrink:0;}
.log-line{font-size:13px;line-height:1.6;}
.l-sys{color:var(--cyan);} .l-play{color:var(--green);} .l-bot{color:#f87171;}
.l-win{color:var(--gold);} .l-truco{color:var(--orange);} .l-code{color:var(--purple);}

/* scrollbar */
::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-track{background:var(--bg2);}
::-webkit-scrollbar-thumb{background:#1e3a5f;border-radius:2px;}
</style>
</head>
<body>
<div id="root">

<!-- HEADER -->
<div id="header">
  <div class="title">🃏 TRUCO DIDÁTICO</div>
  <div class="score-box">
    <div class="score-item">
      <div class="score-label">VOCÊ</div>
      <div class="score-val" id="score-player" style="color:var(--green)">0</div>
    </div>
    <div class="score-item">
      <div class="score-label">RODADA</div>
      <div class="score-val" id="score-round" style="color:var(--gold)">1</div>
    </div>
    <div class="score-item">
      <div class="score-label">BOT</div>
      <div class="score-val" id="score-bot" style="color:var(--magenta)">0</div>
    </div>
  </div>
  <div id="state-badge" class="state-badge state-MENU">MENU</div>
</div>

<!-- BODY -->
<div id="body">

  <!-- LEFT: código ao vivo -->
  <div id="code-panel">
    <div class="code-title">◈ CÓDIGO AO VIVO</div>

    <div class="code-block" id="code-vars">
      <div class="cm">// Cap 11 — Variáveis</div>
      <div><span class="ty">inteiro</span> pontos_jogador <span class="op">=</span> <span class="nm" id="cv-pts">0</span></div>
      <div><span class="ty">inteiro</span> pontos_bot <span class="op">=</span> <span class="nm" id="cv-bpts">0</span></div>
      <div><span class="ty">inteiro</span> valor_aposta <span class="op">=</span> <span class="nm" id="cv-bet">1</span></div>
      <div><span class="ty">logico</span> truco_pedido <span class="op">=</span> <span class="nm" id="cv-truco">falso</span></div>
      <div><span class="ty">cadeia</span> vencedor <span class="op">=</span> <span class="st" id="cv-winner">""</span></div>
    </div>

    <div class="code-block" id="code-ops">
      <div class="cm">// Cap 12 — Operadores</div>
      <div id="cv-formula" style="color:var(--gold)">pontos + aposta</div>
      <div class="cm">// Força da carta:</div>
      <div>forca <span class="op">=</span> rank <span class="op">*</span> <span class="nm">10</span> <span class="op">+</span> naipe</div>
    </div>

    <div class="code-block" id="code-logic">
      <div class="cm">// Cap 13 — Lógica</div>
      <div><span class="kw">se</span> (carta_jog <span class="op">></span> carta_bot)</div>
      <div>&nbsp;&nbsp;<span class="kw">E</span> truco_pedido)</div>
      <div>&nbsp;&nbsp;<span class="fn">ganharRodada</span>(jogador)</div>
      <div id="cv-compare" style="color:var(--purple);font-size:8px;margin-top:2px;"></div>
    </div>

    <div class="code-block" id="code-cond">
      <div class="cm">// Cap 14 — Condicionais</div>
      <div><span class="kw">se</span> (pontos <span class="op">>=</span> <span class="nm">12</span>) {</div>
      <div>&nbsp;&nbsp;<span class="fn">fimDeJogo</span>(<span class="st">"vitória"</span>)</div>
      <div>} <span class="kw">senão se</span> (pontos_bot <span class="op">>=</span> <span class="nm">12</span>) {</div>
      <div>&nbsp;&nbsp;<span class="fn">fimDeJogo</span>(<span class="st">"derrota"</span>)</div>
      <div>}</div>
    </div>

    <div class="code-block" id="code-loop">
      <div class="cm">// Cap 15 — Repetição</div>
      <div><span class="kw">enquanto</span> (jogo_ativo) {</div>
      <div>&nbsp;&nbsp;<span class="fn">processarEntrada</span>()</div>
      <div>&nbsp;&nbsp;<span class="fn">atualizarEstado</span>()</div>
      <div>&nbsp;&nbsp;<span class="fn">renderizarTela</span>()</div>
      <div>}</div>
      <div id="cv-loop" style="color:var(--orange);font-size:8px;margin-top:2px;"></div>
    </div>

    <div class="code-block" id="code-event">
      <div class="cm">// Cap 16 — Eventos</div>
      <div><span class="fn">aoClicar</span>(carta) {</div>
      <div>&nbsp;&nbsp;<span class="kw">se</span> (carta <span class="op">!=</span> <span class="kw">nulo</span>)</div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="fn">jogarCarta</span>(carta)</div>
      <div>}</div>
      <div id="cv-event" style="color:#60a5fa;font-size:8px;margin-top:2px;"></div>
    </div>

    <div class="code-block" id="code-state">
      <div class="cm">// Cap 17 — Estado</div>
      <div><span class="ty">cadeia</span> estado <span class="op">=</span></div>
      <div>&nbsp;&nbsp;<span class="st" id="cv-state">"MENU"</span></div>
      <div class="cm">// MENU→JOGANDO→</div>
      <div class="cm">// TRUCO→FIM_RODADA</div>
    </div>

    <div class="code-block" id="code-score">
      <div class="cm">// Cap 18 — Pontuação</div>
      <div>pontos <span class="op">+=</span></div>
      <div>&nbsp;&nbsp;aposta <span class="op">*</span> rodadas_vencidas</div>
      <div id="cv-score-formula" style="color:#fbbf24;font-size:8px;margin-top:2px;"></div>
    </div>
  </div>

  <!-- CENTER: game -->
  <div id="game-area">
    <div id="canvas-wrap">
      <canvas id="canvas"></canvas>

      <!-- GAME UI -->
      <div id="game-ui">
        <!-- topo -->
        <div class="round-bar">
          <div class="round-info" id="round-label">RODADA 1 · MÃOS: 0/3</div>
          <div style="display:flex;gap:6px;align-items:center;">
            <span style="font-size:15px;color:var(--dim);">APOSTA:</span>
            <span id="bet-label" style="font-family:'Orbitron',sans-serif;font-size:20px;color:var(--orange);font-weight:700;">1 pt</span>
          </div>
          <div>
            <span style="font-size:15px;color:var(--dim);">BOT: </span>
            <span id="bot-lives" class="lives-row">♥♥♥</span>
          </div>
        </div>

        <!-- cartas do bot -->
        <div class="bot-row" id="bot-cards"></div>

        <!-- mesa -->
        <div class="table-row">
          <div class="played-slot" id="slot-player"><span class="slot-label">VOCÊ</span></div>
          <div style="font-family:'Orbitron',sans-serif;font-size:9px;color:var(--dim);">VS</div>
          <div class="played-slot" id="slot-bot"><span class="slot-label">BOT</span></div>
        </div>

        <!-- anúncio truco -->
        <div id="truco-announce">⚡ TRUCO!</div>

        <!-- cartas do jogador -->
        <div class="player-row" id="player-cards"></div>

        <!-- ações -->
        <div class="action-row" id="action-row">
          <button class="btn btn-orange" id="btn-truco" onclick="pedirTruco()">⚡ TRUCO!</button>
          <button class="btn btn-red" id="btn-fugio" onclick="fugir()" style="display:none">🏃 FUGIR</button>
          <button class="btn btn-green" id="btn-aceitar" onclick="aceitarTruco()" style="display:none">✅ ACEITAR</button>
          <button class="btn btn-cyan" id="btn-nova-rodada" onclick="novaRodada()" style="display:none">▶ NOVA RODADA</button>
          <button class="btn btn-cyan" id="btn-novo-jogo" onclick="iniciarJogo()" style="display:none">↺ NOVO JOGO</button>
        </div>
      </div>

      <!-- OVERLAY -->
      <div id="overlay" class="active">
        <div class="ov-box ov-cyan">
          <div class="ov-title" style="color:var(--cyan)">🃏 TRUCO DIDÁTICO</div>
          <div class="ov-sub" style="margin-top:8px;">
            Jogue truco enquanto vê o código sendo executado em tempo real!<br>
            Cada jogada revela um conceito da aula de <b style="color:var(--gold)">Game Logic Mastery</b>.
          </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:8px;font-size:9px;color:var(--dim);text-align:center;">
          <div>🟢 Clique em uma carta para jogar &nbsp;·&nbsp; ⚡ Grite TRUCO para aumentar a aposta</div>
          <div>Primeiro a <span style="color:var(--gold)">12 pontos</span> vence · 3 mãos por rodada</div>
        </div>
        <button class="btn btn-green" style="padding:10px 32px;font-size:13px;letter-spacing:2px;" onclick="iniciarJogo()">▶ INICIAR JOGO</button>
      </div>

    </div><!-- canvas-wrap -->

    <!-- LOG -->
    <div id="log"><div id="log-content"></div></div>
  </div>

  <!-- RIGHT: conceitos -->
  <div id="concept-panel">
    <div class="cpt-title">◈ CONCEITO ATIVO</div>
    <div id="concept-container">
      <div style="padding:16px 10px;font-size:9px;color:var(--dim);text-align:center;">
        Inicie o jogo para ver os conceitos em ação!
      </div>
    </div>
    <div class="cpt-title" style="margin-top:4px;">◈ TODOS OS CAPÍTULOS</div>
    <div style="padding:8px 10px;display:flex;flex-direction:column;gap:6px;font-size:13px;">
      <div style="color:var(--cyan)">Cap 11 · Variáveis</div>
      <div style="color:var(--gold)">Cap 12 · Operadores</div>
      <div style="color:var(--purple)">Cap 13 · Op. Lógicos</div>
      <div style="color:var(--green)">Cap 14 · Condicionais</div>
      <div style="color:var(--orange)">Cap 15 · Repetição</div>
      <div style="color:#60a5fa">Cap 16 · Eventos</div>
      <div style="color:var(--magenta)">Cap 17 · Estados</div>
      <div style="color:#fbbf24">Cap 18 · Pontuação</div>
    </div>
  </div>

</div><!-- body -->
</div><!-- root -->

<script>
// ============================================================
// ── DADOS DO TRUCO ──
// ============================================================

// Hierarquia do truco (do mais forte para o mais fraco)
// 4♣ > 7♥ > A♠ > 7♦ > 3 > 2 > A > K > J > Q > 7 > 6 > 5 > 4
const MANILHA_ORDER = ['4♣','7♥','A♠','7♦'];
const RANK_ORDER    = ['3','2','A','K','J','Q','7']; // 4 só como manilha Zap
const SUITS         = ['♠','♥','♦','♣'];
const RANKS         = ['7','Q','J','K','A','2','3']; // 4 só existe como Zap (manilha)

// ── Variáveis (Cap 11) ──
// inteiro, logico, cadeia, real
let pontos_jogador = 0;   // inteiro
let pontos_bot     = 0;   // inteiro
let valor_aposta   = 1;   // inteiro
let truco_pedido   = false; // logico
let estado         = 'MENU'; // cadeia
let rodada_atual   = 1;
let maos_jogadas   = 0;    // inteiro — quantas mãos já foram na rodada
let maos_jogador   = 0;
let maos_bot       = 0;
let mao_atual      = 0;    // mão corrente (1,2,3)
let jogo_ativo     = false; // logico
let carta_jogador  = null;
let carta_bot_val  = null;
let deck           = [];
let mao_jogador    = [];   // array (lista)
let mao_bot        = [];
let jogador_jogou  = false;
let aguardando_resposta = false;
let conceito_ativo = '';

// ============================================================
// ── CANVAS ──
// ============================================================
const canvas = document.getElementById('canvas');
const ctx    = canvas.getContext('2d');

function resizeCanvas(){
  const w = canvas.parentElement;
  canvas.width  = w.clientWidth;
  canvas.height = w.clientHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Cap 15 — LOOP PRINCIPAL (enquanto jogo_ativo)
function loop(){
  drawBG();
  requestAnimationFrame(loop);
}

function drawBG(){
  const W = canvas.width, H = canvas.height;
  ctx.fillStyle = '#0a0f14';
  ctx.fillRect(0,0,W,H);
  // Mesa de feltro
  const grd = ctx.createRadialGradient(W/2,H/2,20,W/2,H/2,Math.min(W,H)*0.6);
  grd.addColorStop(0,'#0d3320');
  grd.addColorStop(0.7,'#071a0f');
  grd.addColorStop(1,'#0a0f14');
  ctx.fillStyle = grd;
  ctx.beginPath();
  ctx.ellipse(W/2,H/2,W*0.45,H*0.42,0,0,Math.PI*2);
  ctx.fill();
  // borda da mesa
  ctx.strokeStyle = '#1a4a2a';
  ctx.lineWidth = 3;
  ctx.stroke();
  // decoração central
  ctx.save();
  ctx.globalAlpha = 0.07;
  ctx.font = '80px serif';
  ctx.textAlign = 'center';
  ctx.fillStyle = '#39ff14';
  ctx.fillText('🃏', W/2, H/2+30);
  ctx.restore();
  // partículas
  const t = Date.now()*0.001;
  for(let i=0;i<8;i++){
    const px = W/2 + Math.sin(t*0.5+i*0.8)*W*0.38;
    const py = H/2 + Math.cos(t*0.4+i*1.1)*H*0.34;
    ctx.globalAlpha = 0.06+0.04*Math.sin(t+i);
    ctx.fillStyle = i%2===0?'#39ff14':'#00f5ff';
    ctx.beginPath(); ctx.arc(px,py,2,0,Math.PI*2); ctx.fill();
    ctx.globalAlpha = 1;
  }
}
loop();

// ============================================================
// ── BARALHO ──
// ============================================================
function criarBaralho(){
  // Cap 15 — estrutura PARA: para cada rank para cada naipe
  const d = [];
  for(const r of RANKS){         // para (rank em RANKS)
    for(const s of SUITS){       // para (naipe em SUITS)
      d.push({rank:r, suit:s, str: r+s});
    }
  }
  // O 4 só existe como Zap (4♣) — única carta do rank 4 no baralho
  d.push({rank:'4', suit:'♣', str:'4♣'});
  return d;
}

function embaralhar(arr){
  // Cap 12 — operadores, Cap 15 — repetição
  const a = [...arr];
  for(let i = a.length-1; i > 0; i--){  // para i de length-1 até 0
    const j = Math.floor(Math.random() * (i+1));  // operador *
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function forcaCarta(c){
  // Cap 12 — Operadores: cálculo de força
  // Cap 13 — Lógica: OR encadeado
  const mi = MANILHA_ORDER.indexOf(c.str);
  if(mi >= 0) return 100 - mi;  // manilha: força 100, 99, 98, 97
  const ri = RANK_ORDER.indexOf(c.rank);
  if(ri >= 0) return 50 - ri;   // demais: 50 a 41
  return 0;
}

// ============================================================
// ── RENDER CARTAS ──
// ============================================================
const SUIT_COLOR = {'♥':'#ef4444','♦':'#ef4444','♠':'#e2e8f0','♣':'#e2e8f0'};
const MANILHA_META = {
  '4♣': { nome:'ZAP',       bg:'#052e16', brd:'#4ade80', glow:'#4ade80', rankCol:'#4ade80' },
  '7♥': { nome:'COPAS',     bg:'#450a0a', brd:'#f87171', glow:'#f87171', rankCol:'#f87171' },
  'A♠': { nome:'ESPADILHA', bg:'#0c1445', brd:'#818cf8', glow:'#818cf8', rankCol:'#818cf8' },
  '7♦': { nome:'OUROS',     bg:'#431407', brd:'#fb923c', glow:'#fb923c', rankCol:'#fb923c' },
};

function cardHTML(c, isHand=false, idx=0, played=false){
  const isManilha = MANILHA_ORDER.includes(c.str);
  const meta = MANILHA_META[c.str];
  const bg   = isManilha ? meta.bg   : '#1e2d40';
  const brd  = isManilha ? meta.brd  : '#334155';
  const col  = isManilha ? meta.rankCol : (SUIT_COLOR[c.suit] || '#fff');
  const cls  = isHand ? `card-hand${played?' played':''}` : 'card-played';
  const click = isHand && !played ? `onclick="jogarCarta(${idx})"` : '';
  const rank_pos = MANILHA_ORDER.indexOf(c.str) + 1;
  const manTag = isManilha
    ? `<div style="position:absolute;top:2px;left:0;right:0;text-align:center;font-size:9px;font-family:'Orbitron',sans-serif;color:${meta.brd};letter-spacing:0.5px;text-shadow:0 0 4px ${meta.glow};">${meta.nome}</div>
       <div style="position:absolute;bottom:3px;right:4px;font-size:10px;color:${meta.brd};font-weight:700;">#${rank_pos}</div>`
    : '';
  const glowStyle = isManilha ? `box-shadow:0 0 10px ${meta.glow}66,0 4px 12px #000a;border-width:2px;` : '';
  return `<div class="${cls}" style="background:${bg};border-color:${brd};${glowStyle}" ${click}>
    ${manTag}
    <div class="c-rank" style="color:${col};${isManilha?'margin-top:10px;':''}">${c.rank}</div>
    <div class="c-suit" style="color:${col}">${c.suit}</div>
  </div>`;
}

function renderUI(){
  // Cartas do bot (verso)
  const botRow = document.getElementById('bot-cards');
  botRow.innerHTML = mao_bot.map(()=>`<div class="card-back">🂠</div>`).join('');

  // Cartas do jogador
  const playerRow = document.getElementById('player-cards');
  playerRow.innerHTML = mao_jogador.map((c,i)=>cardHTML(c, true, i, false)).join('');

  // Botões
  const cardsDisabled = estado !== 'JOGANDO' || jogador_jogou || aguardando_resposta;
  document.querySelectorAll('.card-hand').forEach(el=>{
    if(cardsDisabled) el.classList.add('disabled');
    else el.classList.remove('disabled');
  });
}

// ============================================================
// ── INICIAR JOGO ──
// ============================================================
function iniciarJogo(){
  // Cap 17 — Estado: MENU → JOGANDO
  setEstado('JOGANDO');
  pontos_jogador = 0; pontos_bot = 0; rodada_atual = 1;
  jogo_ativo = true;
  document.getElementById('overlay').classList.remove('active');
  document.getElementById('btn-novo-jogo').style.display = 'none';
  log('Jogo iniciado! Primeiro a 12 pontos vence.','l-sys');
  highlightCode('code-state', 'Cap 17 — Estado do jogo mudou para JOGANDO');
  showConcept('state');
  updateScores();
  novaRodada();
}

function novaRodada(){
  // Cap 15 — ENQUANTO: o loop do jogo continua enquanto jogo_ativo
  if(!jogo_ativo) return;
  valor_aposta = 1; truco_pedido = false;
  maos_jogadas = 0; maos_jogador = 0; maos_bot = 0; mao_atual = 1;
  carta_jogador = null; carta_bot_val = null;
  jogador_jogou = false; aguardando_resposta = false;
  setEstado('JOGANDO');

  deck = embaralhar(criarBaralho());
  // distribui 3 cartas para cada — Cap 15 (estrutura PARA)
  mao_jogador = [deck.pop(), deck.pop(), deck.pop()];
  mao_bot     = [deck.pop(), deck.pop(), deck.pop()];

  document.getElementById('slot-player').innerHTML = '<span class="slot-label">VOCÊ</span>';
  document.getElementById('slot-bot').innerHTML    = '<span class="slot-label">BOT</span>';
  document.getElementById('btn-truco').style.display = '';
  document.getElementById('btn-fugio').style.display = 'none';
  document.getElementById('btn-aceitar').style.display = 'none';
  document.getElementById('btn-nova-rodada').style.display = 'none';

  updateRoundLabel();
  updateBetLabel();
  renderUI();
  updateCodeVars();

  log(`Rodada ${rodada_atual} iniciada. Suas cartas: ${mao_jogador.map(c=>c.str).join(' ')}`, 'l-sys');
  // Cap 16 — Evento: cartas distribuídas, aguardando clique do jogador
  highlightCode('code-event', 'Cap 16 — Evento: aguardando clique na carta');
  showConcept('event');

  // Cap 15 — loop: atualiza contador
  document.getElementById('cv-loop').textContent = `iteração ${rodada_atual} do enquanto`;
}

// ============================================================
// ── JOGAR CARTA ──
// ============================================================
function jogarCarta(idx){
  if(jogador_jogou || aguardando_resposta || estado !== 'JOGANDO') return;
  carta_jogador = mao_jogador[idx];
  jogador_jogou = true;

  // Cap 16 — EVENTO: clique na carta
  document.getElementById('cv-event').textContent = `evento: carta ${carta_jogador.str} clicada`;
  highlightCode('code-event', 'Cap 16 — Evento disparado: jogarCarta()');
  showConcept('event');
  log(`▶ Você jogou: ${carta_jogador.str}`, 'l-play');

  // Mostra carta na mesa
  const slotP = document.getElementById('slot-player');
  slotP.innerHTML = cardHTML(carta_jogador) + '<span class="slot-label">VOCÊ</span>';

  // Remove da mão (visualmente)
  renderUI();
  document.getElementById('player-cards').children[idx]?.classList.add('played');

  // Cap 15 — PARA: bot escolhe carta (após delay curto)
  setTimeout(botJogar, 700);
}

function botJogar(){
  // Cap 14 — CONDICIONAL: bot decide qual carta jogar
  // Lógica simples: se tem carta mais forte que a do jogador, joga ela; senão joga a mais fraca
  const forca_jog = forcaCarta(carta_jogador);

  // Cap 13 — Operadores lógicos: filtra cartas mais fortes
  const mais_fortes = mao_bot.filter(c => forcaCarta(c) > forca_jog);  // AND implícito
  let escolha;
  if(mais_fortes.length > 0){                              // Cap 14 — SE
    // escolhe a mais fraca das mais fortes (economizar manilha)
    escolha = mais_fortes.sort((a,b)=>forcaCarta(a)-forcaCarta(b))[0];
    highlightCode('code-cond', 'Cap 14 — SE: bot tem carta mais forte → joga ela');
  } else {                                                 // Cap 14 — SENÃO
    // joga a mais fraca
    escolha = mao_bot.sort((a,b)=>forcaCarta(a)-forcaCarta(b))[0];
    highlightCode('code-cond', 'Cap 14 — SENÃO: sem carta mais forte → joga a mais fraca');
  }
  showConcept('cond');

  carta_bot_val = escolha;
  mao_bot.splice(mao_bot.indexOf(escolha), 1);

  const slotB = document.getElementById('slot-bot');
  slotB.innerHTML = cardHTML(escolha) + '<span class="slot-label">BOT</span>';
  log(`🤖 Bot jogou: ${escolha.str}`, 'l-bot');

  setTimeout(resolverMao, 600);
}

// ============================================================
// ── RESOLVER MÃO ──
// ============================================================
function resolverMao(){
  // Cap 12 — OPERADORES: calcula e compara forças
  const fj = forcaCarta(carta_jogador);
  const fb = forcaCarta(carta_bot_val);

  // Cap 12: operadores de comparação
  document.getElementById('cv-compare').textContent =
    `${carta_jogador.str}(${fj}) vs ${carta_bot_val.str}(${fb})`;
  highlightCode('code-ops', `Cap 12 — Operadores: ${fj} > ${fb} ?`);
  showConcept('op');

  let venc_mao = '';
  // Cap 13 — OPERADORES LÓGICOS e Cap 14 — CONDICIONAIS
  if(fj > fb){           // SE fj > fb
    venc_mao = 'jogador';
    maos_jogador++;
    log(`✅ Você venceu a mão ${mao_atual}! (${carta_jogador.str} > ${carta_bot_val.str})`, 'l-win');
    document.getElementById('slot-player').querySelector('.card-played')?.classList.add('winner');
  } else if(fb > fj){    // SENÃO SE fb > fj
    venc_mao = 'bot';
    maos_bot++;
    log(`❌ Bot venceu a mão ${mao_atual}. (${carta_bot_val.str} > ${carta_jogador.str})`, 'l-bot');
    document.getElementById('slot-bot').querySelector('.card-played')?.classList.add('winner');
  } else {               // SENÃO (empate)
    venc_mao = 'empate';
    log(`🤝 Empate na mão ${mao_atual}.`, 'l-sys');
  }

  mao_atual++;
  maos_jogadas++;
  jogador_jogou = false;
  carta_jogador = null;
  carta_bot_val = null;
  updateRoundLabel();

  // Cap 14 + Cap 13 — SE (condição de vitória da rodada)
  // Vence rodada: 2 mãos OU 1 mão (se a outra for empate)
  const venceu_rodada = verificarVitoriaRodada();

  if(venceu_rodada){
    setTimeout(()=>finalizarRodada(venceu_rodada), 800);
  } else if(maos_jogadas >= 3 || mao_bot.length === 0){
    // empatou tudo — quem ganhou 1ª mão vence
    setTimeout(()=>finalizarRodada('empate_geral'), 800);
  } else {
    // próxima mão
    setTimeout(()=>{
      document.getElementById('slot-player').innerHTML = '<span class="slot-label">VOCÊ</span>';
      document.getElementById('slot-bot').innerHTML    = '<span class="slot-label">BOT</span>';
      renderUI();
      log(`Mão ${mao_atual}: jogue sua próxima carta.`, 'l-sys');
      highlightCode('code-event', 'Cap 16 — Evento: próxima mão, aguardando input');
      showConcept('event');
    }, 500);
  }
}

function verificarVitoriaRodada(){
  // Cap 14 — CONDICIONAIS aninhadas
  // Cap 13 — OPERADORES LÓGICOS (E, OU)
  highlightCode('code-logic','Cap 13 — Operadores Lógicos: verificando condição de vitória');
  showConcept('logic');

  if(maos_jogador >= 2) return 'jogador';   // SE maos_jogador >= 2
  if(maos_bot >= 2)     return 'bot';       // SE maos_bot >= 2
  // Caso especial: 1ª mão decide em empates posteriores
  if(maos_jogadas === 2 && maos_jogador === 1 && maos_bot === 0) return 'jogador';
  if(maos_jogadas === 2 && maos_bot === 1 && maos_jogador === 0) return 'bot';
  return null;
}

// ============================================================
// ── FINALIZAR RODADA ──
// ============================================================
function finalizarRodada(venc){
  // Cap 18 — PONTUAÇÃO: pontos = pontos + aposta * resultado
  // Cap 12 — OPERADORES: +, *
  let pts = 0;
  if(venc === 'jogador'){
    pts = valor_aposta;
    pontos_jogador += pts;      // Cap 12: soma
    // Cap 18: fórmula visual
    document.getElementById('cv-score-formula').textContent =
      `${pontos_jogador - pts} + ${valor_aposta} = ${pontos_jogador}`;
    highlightCode('code-score', `Cap 18 — Pontuação: +${pts} pontos! pontos = pontos + aposta`);
    showConcept('score');
    log(`🏆 Você venceu a rodada ${rodada_atual}! +${pts} ponto(s). Total: ${pontos_jogador}`, 'l-win');
  } else if(venc === 'bot'){
    pts = valor_aposta;
    pontos_bot += pts;
    document.getElementById('cv-score-formula').textContent =
      `bot: ${pontos_bot - pts} + ${valor_aposta} = ${pontos_bot}`;
    highlightCode('code-score', `Cap 18 — Pontuação: bot +${pts} pontos`);
    showConcept('score');
    log(`😔 Bot venceu a rodada ${rodada_atual}. Bot +${pts}. Total bot: ${pontos_bot}`, 'l-bot');
  } else {
    log(`🤝 Rodada ${rodada_atual} empatada. Nenhum ponto.`, 'l-sys');
  }

  updateScores();
  rodada_atual++;

  // Cap 14 — CONDICIONAL: verificar fim de jogo
  highlightCode('code-cond', 'Cap 14 — SE: verificando se alguém atingiu 12 pontos');
  showConcept('cond');

  if(pontos_jogador >= 12){        // SE pontos_jogador >= 12
    setTimeout(()=>fimDeJogo('vitória'), 800);
  } else if(pontos_bot >= 12){     // SENÃO SE pontos_bot >= 12
    setTimeout(()=>fimDeJogo('derrota'), 800);
  } else {
    document.getElementById('btn-nova-rodada').style.display = '';
    document.getElementById('btn-truco').style.display = 'none';
  }
}

// ============================================================
// ── TRUCO ──
// ============================================================
function pedirTruco(){
  if(truco_pedido || estado !== 'JOGANDO') return;

  // Cap 17 — ESTADO: JOGANDO → TRUCO
  setEstado('TRUCO');
  truco_pedido = true;
  aguardando_resposta = true;
  valor_aposta = valor_aposta === 1 ? 3 : valor_aposta + 3;

  document.getElementById('cv-truco').textContent = 'verdadeiro';
  document.getElementById('cv-bet').textContent   = valor_aposta;
  highlightCode('code-vars', 'Cap 11 — Variável lógica: truco_pedido = verdadeiro');
  showConcept('var');

  // Cap 16 — EVENTO disparado
  document.getElementById('cv-event').textContent = 'evento: TRUCO pedido pelo jogador';

  // Mostra anúncio visual
  const ann = document.getElementById('truco-announce');
  ann.textContent = '⚡ TRUCO!';
  ann.style.display = 'block';
  setTimeout(()=>{ ann.style.display='none'; }, 1200);

  document.getElementById('btn-truco').style.display   = 'none';
  document.getElementById('btn-fugio').style.display   = '';
  document.getElementById('btn-aceitar').style.display = '';
  updateBetLabel();
  log(`⚡ TRUCO! Aposta aumentou para ${valor_aposta} pontos.`, 'l-truco');

  // Bot decide — Cap 14 condicional
  setTimeout(botResponderTruco, 1000);
}

function botResponderTruco(){
  // Cap 14 — CONDICIONAL: bot aceita se tem carta forte (força > 60)
  const temCarta = mao_bot.some(c => forcaCarta(c) > 55);  // Cap 13 — lógico
  if(temCarta){                                              // Cap 14 — SE
    log('🤖 Bot ACEITOU o truco!', 'l-bot');
    highlightCode('code-cond', 'Cap 14 — SE: bot tem carta forte → aceita truco');
    aceitarTruco();
  } else {                                                   // Cap 14 — SENÃO
    log('🤖 Bot FUGIU do truco!', 'l-bot');
    highlightCode('code-cond', 'Cap 14 — SENÃO: bot sem carta forte → foge');
    // bot foge: jogador ganha 1 ponto
    aguardando_resposta = false;
    setEstado('JOGANDO');
    document.getElementById('btn-fugio').style.display   = 'none';
    document.getElementById('btn-aceitar').style.display = 'none';
    document.getElementById('btn-truco').style.display   = '';
    valor_aposta = 1; truco_pedido = false;
    pontos_jogador += 1;
    updateScores();
    log('🏆 Bot correu do truco! +1 ponto para você.', 'l-win');
    document.getElementById('cv-score-formula').textContent = `${pontos_jogador-1} + 1 = ${pontos_jogador}`;
    if(pontos_jogador >= 12) setTimeout(()=>fimDeJogo('vitória'),600);
    else { document.getElementById('btn-nova-rodada').style.display=''; document.getElementById('btn-truco').style.display='none'; }
  }
}

function aceitarTruco(){
  aguardando_resposta = false;
  setEstado('JOGANDO');
  document.getElementById('btn-fugio').style.display   = 'none';
  document.getElementById('btn-aceitar').style.display = 'none';
  document.getElementById('btn-truco').style.display   = '';
  updateBetLabel();
  log(`✅ Truco aceito! Quem vencer a rodada ganha ${valor_aposta} pontos.`, 'l-truco');
  renderUI();
}

function fugir(){
  // Jogador fugiu do truco do bot (se o bot pedisse — simplificado aqui)
  aguardando_resposta = false;
  setEstado('JOGANDO');
  document.getElementById('btn-fugio').style.display   = 'none';
  document.getElementById('btn-aceitar').style.display = 'none';
  document.getElementById('btn-truco').style.display   = '';
  pontos_bot += 1;
  valor_aposta = 1; truco_pedido = false;
  updateScores();
  log('🏃 Você fugiu do truco. Bot +1 ponto.', 'l-bot');
  if(pontos_bot >= 12) setTimeout(()=>fimDeJogo('derrota'),600);
  else { document.getElementById('btn-nova-rodada').style.display=''; document.getElementById('btn-truco').style.display='none'; }
}

// ============================================================
// ── FIM DE JOGO ──
// ============================================================
function fimDeJogo(resultado){
  // Cap 17 — ESTADO: → FIM
  setEstado('FIM');
  jogo_ativo = false;

  const overlay = document.getElementById('overlay');
  overlay.classList.add('active');
  overlay.innerHTML = '';

  const won = resultado === 'vitória';
  const box = document.createElement('div');
  box.className = `ov-box ${won ? 'ov-gold' : 'ov-red'}`;
  box.innerHTML = `
    <div class="ov-title" style="color:${won?'var(--gold)':'var(--magenta)'}">${won?'🏆 VITÓRIA!':'💀 DERROTA'}</div>
    <div class="ov-sub" style="margin-top:8px;">
      Você: <b style="color:var(--green)">${pontos_jogador}</b> pts &nbsp;·&nbsp; Bot: <b style="color:var(--magenta)">${pontos_bot}</b> pts<br>
      <span style="color:var(--dim)">Rodadas jogadas: ${rodada_atual-1}</span>
    </div>`;
  overlay.appendChild(box);

  const resumo = document.createElement('div');
  resumo.style.cssText = 'font-size:9px;color:var(--dim);text-align:center;max-width:360px;line-height:1.8;';
  resumo.innerHTML = `
    <b style="color:var(--cyan)">Conceitos aplicados nesse jogo:</b><br>
    Cap 11 Variáveis · Cap 12 Operadores · Cap 13 Lógica<br>
    Cap 14 Condicionais · Cap 15 Repetição · Cap 16 Eventos<br>
    Cap 17 Estados · Cap 18 Pontuação`;
  overlay.appendChild(resumo);

  const btn = document.createElement('button');
  btn.className = 'btn btn-cyan';
  btn.style.cssText = 'padding:10px 28px;font-size:12px;';
  btn.textContent = '↺ JOGAR NOVAMENTE';
  btn.onclick = iniciarJogo;
  overlay.appendChild(btn);

  log(`🎮 Fim de jogo! Resultado: ${resultado}. Você: ${pontos_jogador} · Bot: ${pontos_bot}`, 'l-win');
  highlightCode('code-cond', 'Cap 14 — Condicional: pontos >= 12 → fimDeJogo()');
  showConcept('cond');
}

// ============================================================
// ── CONCEITOS DIDÁTICOS ──
// ============================================================
const CONCEPTS = {
  var: {
    cls:'cpt-var', cap:'Cap 11 — Variáveis',
    text:`<b>inteiro</b> pontos_jogador = 0<br>
          <b>logico</b> truco_pedido = falso<br>
          <b>cadeia</b> estado = "JOGANDO"<br><br>
          Variáveis são "caixas na memória" que guardam o estado do jogo.
          Cada jogada altera o <em>valor</em> dessas caixas.`
  },
  op: {
    cls:'cpt-op', cap:'Cap 12 — Operadores Matemáticos',
    text:`forca = rank <b>*</b> 10 <b>+</b> naipe<br>
          pontos <b>+=</b> aposta<br><br>
          Operadores calculam dano, força de carta e pontuação.
          A ordem importa: <b>*</b> antes de <b>+</b>!`
  },
  logic: {
    cls:'cpt-logic', cap:'Cap 13 — Operadores Lógicos',
    text:`SE (forca_jog <b>></b> forca_bot)<br>
          &nbsp;&nbsp;<b>E</b> truco_pedido == verdadeiro<br><br>
          <b>E (AND):</b> as duas condições devem ser verdadeiras.<br>
          <b>OU (OR):</b> basta uma ser verdadeira.<br>
          Usados para decidir quem vence cada mão.`
  },
  cond: {
    cls:'cpt-cond', cap:'Cap 14 — Estruturas Condicionais',
    text:`<b>se</b> (pontos >= 12) { vitória() }<br>
          <b>senão se</b> (pts_bot >= 12) { derrota() }<br>
          <b>senão</b> { continuar() }<br><br>
          O jogo toma caminhos diferentes baseado
          nas ações do jogador — a "encruzilhada" do código.`
  },
  loop: {
    cls:'cpt-loop', cap:'Cap 15 — Repetição',
    text:`<b>para</b> (rank em RANKS) { embaralhar() }<br>
          <b>enquanto</b> (jogo_ativo) { gameLoop() }<br><br>
          O loop principal roda 60x por segundo.
          O embaralhamento usa <b>para</b> para percorrer todas as cartas.`
  },
  event: {
    cls:'cpt-event', cap:'Cap 16 — Eventos',
    text:`<b>aoClicar</b>(carta) {<br>
          &nbsp;&nbsp;se (carta != nulo)<br>
          &nbsp;&nbsp;&nbsp;&nbsp;jogarCarta(carta)<br>
          }<br><br>
          O jogo não avança sozinho: ele espera seu
          clique, captura o evento e reage a ele.`
  },
  state: {
    cls:'cpt-state', cap:'Cap 17 — Estados de Jogo',
    text:`MENU <b>→</b> JOGANDO <b>→</b> TRUCO <b>→</b> FIM<br><br>
          <b>cadeia</b> estado = "JOGANDO"<br><br>
          Cada estado define o que o jogador pode fazer.
          "TRUCO" bloqueia jogar cartas; "FIM" encerra o loop.`
  },
  score: {
    cls:'cpt-score', cap:'Cap 18 — Sistema de Pontuação',
    text:`pontos = pontos <b>+</b> (aposta <b>*</b> rodadas_vencidas)<br><br>
          A fórmula usa multiplicação para aumentar a recompensa
          quando o jogador arriscou no truco.<br>
          <em>Recorde Atual: ${Math.max(pontos_jogador, pontos_bot)}</em>`
  }
};

function showConcept(key){
  if(conceito_ativo === key) return;
  conceito_ativo = key;
  const c = CONCEPTS[key];
  if(!c) return;
  document.getElementById('concept-container').innerHTML = `
    <div class="concept-card ${c.cls} active">
      <h4>${c.cap}</h4>
      <div style="margin-top:4px;">${c.text}</div>
    </div>`;
}

function highlightCode(blockId, tooltip){
  document.querySelectorAll('.code-block').forEach(b=>b.classList.remove('active-concept'));
  const el = document.getElementById(blockId);
  if(el){ el.classList.add('active-concept'); }
  log(`💡 ${tooltip}`, 'l-code');
}

// ============================================================
// ── HELPERS ──
// ============================================================
function setEstado(novo){
  estado = novo;
  document.getElementById('cv-state').textContent = `"${novo}"`;
  const badge = document.getElementById('state-badge');
  badge.textContent = novo;
  badge.className = `state-badge state-${novo.replace(' ','_')}`;
}

function updateScores(){
  document.getElementById('score-player').textContent = pontos_jogador;
  document.getElementById('score-bot').textContent    = pontos_bot;
  document.getElementById('score-round').textContent  = rodada_atual;
  document.getElementById('cv-pts').textContent       = pontos_jogador;
  document.getElementById('cv-bpts').textContent      = pontos_bot;
  updateCodeVars();
}

function updateCodeVars(){
  document.getElementById('cv-bet').textContent    = valor_aposta;
  document.getElementById('cv-truco').textContent  = truco_pedido ? 'verdadeiro' : 'falso';
  document.getElementById('cv-winner').textContent = `"${estado}"`;
  document.getElementById('cv-formula').textContent = `${pontos_jogador} + ${valor_aposta}`;
}

function updateRoundLabel(){
  document.getElementById('round-label').textContent =
    `RODADA ${rodada_atual} · MÃO: ${mao_atual-1}/3`;
}
function updateBetLabel(){
  document.getElementById('bet-label').textContent = `${valor_aposta} pt${valor_aposta>1?'s':''}`;
  document.getElementById('cv-bet').textContent = valor_aposta;
}

function log(msg, cls='l-sys'){
  const d = document.getElementById('log-content');
  const line = document.createElement('div');
  line.className = 'log-line '+cls;
  line.textContent = msg;
  d.prepend(line);
  while(d.children.length > 40) d.removeChild(d.lastChild);
}
</script>
</body>
</html>
"""

components.html(GAME, height=820, scrolling=False)
