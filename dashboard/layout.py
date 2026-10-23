"""Componentes de apresentação compacta; sem cálculos físicos."""


import math
import json


def preparar_contrato_trajetoria(comprimento_m, desnivel_m, theta_graus, estados,
                                 modo="livre", velocidade_alvo=0.02,
                                 massa_kg=None, cr=None, raio_tambor_m=0.05,
                                 relacao_transmissao=5.0, eficiencia_hypotetica=0.55):
    """Valida e serializa a fronteira Python -> componente visual.

    A física permanece no simulador; este contrato contém somente amostras já
    calculadas e metadados para reprodução local no navegador.
    """
    L = float(comprimento_m)
    H = float(desnivel_m)
    theta = float(theta_graus)
    if not all(math.isfinite(v) for v in (L, H, theta)) or L <= 0 or H < 0 or not 0 < theta < 90:
        raise ValueError("geometria inválida para o contrato de trajetória")
    samples = []
    for estado in estados:
        row = {"t_s": float(estado.tempo_s), "s_m": float(estado.posicao_m),
               "v_track_m_s": float(estado.velocidade_m_s),
               "energy_remaining_J": float(estado.energia.restante_J)}
        if not all(math.isfinite(v) for v in row.values()):
            raise ValueError("amostra não finita")
        samples.append(row)
    if modo == "alvo":
        if velocidade_alvo <= 0 or not math.isfinite(float(velocidade_alvo)):
            raise ValueError("velocidade-alvo inválida")
        n = max(len(samples), 2)
        e0 = samples[0]["energy_remaining_J"] if samples else 0.0
        dur = L / float(velocidade_alvo)
        samples = [{"t_s": dur * i / (n - 1), "s_m": L * i / (n - 1),
                    "v_track_m_s": float(velocidade_alvo),
                    "energy_remaining_J": max(0.0, e0 * (1 - i / (n - 1)))} for i in range(n)]
    previous_t = -math.inf
    for row in samples:
        if row["t_s"] < previous_t or row["s_m"] < -1e-9 or row["s_m"] > L + 1e-9:
            raise ValueError("amostras fora de ordem ou fora do percurso")
        previous_t = row["t_s"]
        row["s_m"] = max(0.0, min(L, row["s_m"]))
    if not samples:
        samples = [{"t_s": 0.0, "s_m": 0.0, "v_track_m_s": 0.0, "energy_remaining_J": 0.0}]
    return {"geometry": {"L_m": L, "H_m": H, "theta_deg": theta,
                          "travel_start_m": 0.0, "travel_end_m": L},
            "mechanical": {"mass_kg": massa_kg, "rolling_coefficient": cr,
                           "drum_radius_m": raio_tambor_m, "gear_ratio": relacao_transmissao,
                           "efficiency_hypothesis": eficiencia_hypotetica},
            "trajectory": {"mode": "target_hypothesis" if modo == "alvo" else "free",
                            "samples": samples},
            "metadata": {"model_classification": "CALCULADO" if modo != "alvo" else "HIPÓTESE CINEMÁTICA",
                         "source": "simulation.simulator" if modo != "alvo" else "velocidade-alvo configurada",
                         "notes": "JavaScript apenas interpola amostras; não reconstrói a física."}}


def svg_rampa_compacta(comprimento_m, desnivel_m, progresso=0.52, theta_graus=None, posicao_m=None):
    """Retorna uma representação SVG responsiva da rampa e do tambor."""
    p = max(0.08, min(0.92, float(progresso)))
    theta = math.radians(theta_graus) if theta_graus is not None else math.atan2(desnivel_m, comprimento_m)
    distancia_horizontal = comprimento_m * math.cos(theta)
    escala = min(520.0 / max(distancia_horizontal, 0.001), 185.0 / max(desnivel_m, 0.001))
    x0, y0 = 95, 260
    x1, y1 = x0 + distancia_horizontal * escala, y0 - desnivel_m * escala
    p_fisico = max(0.0, min(comprimento_m, posicao_m if posicao_m is not None else p * comprimento_m))
    xm = x0 + p_fisico * math.cos(theta) * escala
    ym = y0 - p_fisico * math.sin(theta) * escala
    barra = max(0.5, min(5.0, 1.0 / escala))
    return f"""
    <div class='gravbat-rampa'>
      <svg viewBox='0 0 760 300' role='img' aria-label='Representação esquemática da rampa, massa, cabo e tambor'>
        <line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y1}' stroke='#8091aa' stroke-width='14' stroke-linecap='round'/>
        <line x1='{x0}' y1='{y0 + 26}' x2='{x1}' y2='{y1 + 26}' stroke='#273342' stroke-width='3'/>
        <line x1='{xm}' y1='{ym}' x2='{x1}' y2='{y1}' stroke='#e2a84a' stroke-width='5'/>
        <rect x='{xm - 28}' y='{ym - 20}' width='56' height='40' rx='9' fill='#c98236' stroke='#f1c27a' stroke-width='3' transform='rotate(-18 {xm} {ym})'/>
        <circle cx='{x1 + 40}' cy='{y1}' r='32' fill='#263347' stroke='#8fa1bd' stroke-width='8'/>
        <circle cx='{x1 + 40}' cy='{y1}' r='10' fill='#8fa1bd'/>
        <line x1='{x1 + 40}' y1='{y1 + 32}' x2='{x1 + 40}' y2='{y0 + 18}' stroke='#4c5b70' stroke-width='2' stroke-dasharray='7 7'/>
        <path d='M 250 170 L 205 190 L 250 210' fill='none' stroke='#3ac2a2' stroke-width='7' stroke-linecap='round' stroke-linejoin='round'/>
        <text x='160' y='175' fill='#dce5f2' font-size='20' font-family='sans-serif'>Descida</text>
        <text x='330' y='285' fill='#b4c0d0' font-size='18' font-family='sans-serif'>L = {comprimento_m:.2f} m</text>
        <line x1='{x1 + 18}' y1='{y0}' x2='{x1 + 18}' y2='{y1}' stroke='#b4c0d0' stroke-width='2' stroke-dasharray='6 6'/>
        <text x='{x1 + 27}' y='{(y0 + y1) / 2:.1f}' fill='#b4c0d0' font-size='16' font-family='sans-serif'>H = {desnivel_m:.2f} m</text>
        <text x='{x0 + 10}' y='{y0 - 12}' fill='#b4c0d0' font-size='15' font-family='sans-serif'>θ = {math.degrees(theta):.1f}°</text>
        <line x1='{x0}' y1='285' x2='{x0 + 1.0 * escala}' y2='285' stroke='#dce5f2' stroke-width='3'/>
        <text x='{x0}' y='298' fill='#b4c0d0' font-size='13' font-family='sans-serif'>1 m</text>
        <text x='{xm - 23}' y='{ym - 30}' fill='#dce5f2' font-size='14' font-family='sans-serif'>massa</text>
        <text x='{x1 + 20}' y='{y1 - 45}' fill='#dce5f2' font-size='14' font-family='sans-serif'>tambor</text>
      </svg>
    </div>
    """


def animacao_interativa_html(comprimento_m, desnivel_m, theta_graus, estados, modo="livre", velocidade_alvo=0.02, massa_kg=None, cr=None):
    """Componente local: física vem do Python; reprodução usa requestAnimationFrame."""
    theta = math.radians(theta_graus)
    d = comprimento_m * math.cos(theta)
    escala = min(520 / max(d, .001), 185 / max(desnivel_m, .001))
    x0, y0 = 95, 260
    x1, y1 = x0 + d * escala, y0 - desnivel_m * escala
    nx, ny = -math.sin(theta) * 22, math.cos(theta) * 22
    contrato = preparar_contrato_trajetoria(comprimento_m, desnivel_m, theta_graus, estados, modo, velocidade_alvo, massa_kg, cr)
    payload = json.dumps(contrato, separators=(",", ":"), ensure_ascii=False)
    return f"""
    <style>
      .gbanim{{font-family:Arial,sans-serif;color:#dbe5f0;background:#0d1118;border:1px solid #29384b;border-radius:12px;padding:12px}}
      .gbgrid{{display:grid;grid-template-columns:1.15fr .9fr;gap:10px}} .gbanim svg{{width:100%;height:300px;display:block}} .gbctrl{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
      .gbctrl button,.gbctrl select{{background:#182231;color:#eaf1f8;border:1px solid #4b5d72;border-radius:6px;padding:6px 10px}}
      .gbctrl input{{accent-color:#3ac2a2;flex:1;min-width:180px}} .gbvals{{display:flex;gap:24px;margin-top:8px;font-size:13px}}
      .gbvals b{{color:#fff}}
    </style>
    <div class="gbanim">
      <div class="gbgrid"><svg viewBox="0 0 900 300" aria-label="Animação da rampa">
        <line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#8091aa" stroke-width="10" stroke-linecap="round"/>
        <line x1="{x0+nx}" y1="{y0+ny}" x2="{x1+nx}" y2="{y1+ny}" stroke="#8091aa" stroke-width="10" stroke-linecap="round"/>
        <line id="gb-cabo" x1="{x1}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#e2a84a" stroke-width="5"/>
        <g id="gb-carro" transform="translate({x0},{y0}) rotate({-math.degrees(theta)})">
          <rect id="gb-massa" x="-28" y="-12" width="56" height="24" rx="7" fill="#c98236" stroke="#f1c27a" stroke-width="3"/>
          <circle cx="-20" cy="0" r="8" fill="#b8c7d9" stroke="#43546b" stroke-width="3"/>
          <circle cx="20" cy="22" r="8" fill="#b8c7d9" stroke="#43546b" stroke-width="3"/>
        </g>
        <line x1="{x1+40}" y1="{y1+32}" x2="{x1+40}" y2="{y1+105}" stroke="#8fa1bd" stroke-width="5"/>
        <circle cx="{x1+40}" cy="{y1}" r="32" fill="#263347" stroke="#8fa1bd" stroke-width="8"/><circle cx="{x1+40}" cy="{y1}" r="10" fill="#8fa1bd"/>
        <circle id="gb-gear-big" cx="{x1+40}" cy="{y1+67}" r="27" fill="#25344a" stroke="#9db0c9" stroke-width="4"/><circle id="gb-gear-small" cx="{x1+92}" cy="{y1+67}" r="15" fill="#25344a" stroke="#9db0c9" stroke-width="4"/>
        <rect x="{x1+110}" y="{y1+43}" width="90" height="48" rx="8" fill="#182b35" stroke="#3ac2a2" stroke-width="2"/><text x="{x1+123}" y="{y1+72}" fill="#dce5f2" font-size="14">gerador</text>
        <path d="M 250 170 L 205 190 L 250 210" fill="none" stroke="#3ac2a2" stroke-width="7"/>
        <text x="150" y="175" fill="#dce5f2" font-size="20">Descida</text>
        <text x="{x0+20}" y="292" fill="#b4c0d0" font-size="16">L = {comprimento_m:.2f} m · H = {desnivel_m:.2f} m · θ = {theta_graus:.1f}°</text>
        <text x="{x1+10}" y="{y1+135}" fill="#8fa1bd" font-size="12">transmissão esquemática · G = 5:1</text>
      </svg><svg id="gb-chart" viewBox="0 0 520 300" aria-label="Gráfico sincronizado"><line x1="55" y1="250" x2="500" y2="250" stroke="#718096"/><line x1="55" y1="25" x2="55" y2="250" stroke="#718096"/><polyline id="gb-curve" fill="none" stroke="#45b8e5" stroke-width="4"/><line id="gb-marker" x1="55" y1="25" x2="55" y2="250" stroke="#3ac2a2" stroke-dasharray="6 5" stroke-width="2"/><circle id="gb-point" cx="55" cy="250" r="7" fill="#3ac2a2"/><text id="gb-chart-title" x="70" y="20" fill="#dce5f2" font-size="17">Velocidade × tempo</text><text id="gb-chart-x" x="65" y="275" fill="#b4c0d0" font-size="13">tempo físico (s)</text><text id="gb-chart-y" x="8" y="35" fill="#b4c0d0" font-size="13">v (m/s)</text></svg></div>
      <select id="gb-chart-select"><option value="speed">Velocidade × tempo</option><option value="energy">Energia × posição</option></select>
      <div class="gbctrl"><button id="gb-play">▶ Executar</button><button id="gb-pause">Ⅱ Pausar</button><button id="gb-reset">↺ Reiniciar</button><select id="gb-speed"><option>0.25</option><option>0.5</option><option selected>1</option><option>2</option><option>5</option></select><input id="gb-seek" type="range" min="0" max="1" step="0.001" value="0"></div>
      <div class="gbvals"><span>Tempo <b id="gb-t">0.00 s</b></span><span>Posição <b id="gb-s">0.00 m</b></span><span>Velocidade <b id="gb-v">0.00 m/s</b></span></div>
    </div>
    <script>
    (()=>{{const contract={payload}, data=contract.trajectory.samples.map(a=>({{t:a.t_s,s:a.s_m,v:a.v_track_m_s,energy:a.energy_remaining_J}})), car=document.getElementById('gb-carro'), cable=document.getElementById('gb-cabo'), gearBig=document.getElementById('gb-gear-big'), gearSmall=document.getElementById('gb-gear-small'), seek=document.getElementById('gb-seek'), play=document.getElementById('gb-play'), pause=document.getElementById('gb-pause'), reset=document.getElementById('gb-reset'), speed=document.getElementById('gb-speed'), chartSelect=document.getElementById('gb-chart-select'), curve=document.getElementById('gb-curve'), marker=document.getElementById('gb-marker'), point=document.getElementById('gb-point'), title=document.getElementById('gb-chart-title'), chartX=document.getElementById('gb-chart-x'), chartY=document.getElementById('gb-chart-y'); const tEl=document.getElementById('gb-t'),sEl=document.getElementById('gb-s'),vEl=document.getElementById('gb-v'); const x0={x0},y0={y0},x1={x1},y1={y1},L=contract.geometry.L_m,theta=contract.geometry.theta_deg*Math.PI/180,tx=x1-11*Math.sin(theta),ty=y1+11*Math.cos(theta); let clock=0, running=false, last=null; const end=data[data.length-1]?.t||0; function sample(t){{if(!data.length)return {{t:0,s:0,v:0,energy:0}}; if(t<=data[0].t)return data[0]; for(let i=1;i<data.length;i++){{if(t<=data[i].t){{const a=data[i-1],b=data[i],q=(t-a.t)/Math.max(b.t-a.t,1e-9);return {{t,s:a.s+q*(b.s-a.s),v:a.v+q*(b.v-a.v),energy:a.energy+q*(b.energy-a.energy)}};}}}} return data[data.length-1];}} function draw(t){{const z=sample(t),u=Math.max(0,Math.min(1,z.s/L)),x=x1+u*(x0-x1),y=y1+u*(y0-y1),nx=-Math.sin(theta),ny=Math.cos(theta),ax=x+11*nx,ay=y+11*ny; car.setAttribute('transform','translate('+x+','+y+') rotate('+(-theta*180/Math.PI)+')'); cable.setAttribute('x1',ax);cable.setAttribute('y1',ay);cable.setAttribute('x2',x1);cable.setAttribute('y2',y1);gearBig.setAttribute('transform','rotate('+ (z.s/0.05*180/Math.PI) +' '+(x1+40)+' '+(y1+67)+')');gearSmall.setAttribute('transform','rotate('+ (-z.s/0.05*180/Math.PI*5) +' '+(x1+92)+' '+(y1+67)+')');seek.value=(end?t/end:0);tEl.textContent=z.t.toFixed(2)+' s';sEl.textContent=z.s.toFixed(2)+' m';vEl.textContent=z.v.toFixed(3)+' m/s'; const energy=chartSelect.value==='energy'; const max=energy?Math.max(...data.map(a=>a.energy),1):Math.max(...data.map(a=>a.v),1e-6); const points=data.map(a=>{{const cx=55+(energy?a.s/L:a.t/end)*445,cy=250-(energy?a.energy:max===0?0:a.v)/max*220;return cx.toFixed(1)+','+cy.toFixed(1)}}).join(' ');curve.setAttribute('points',points);const cx=55+(energy?z.s/L:z.t/end)*445,cy=250-(energy?z.energy:z.v)/max*220;marker.setAttribute('x1',cx);marker.setAttribute('x2',cx);point.setAttribute('cx',cx);point.setAttribute('cy',cy);title.textContent=energy?'Energia × posição':'Velocidade × tempo';chartX.textContent=energy?'posição (m)':'tempo físico (s)';chartY.textContent=energy?'energia restante (J)':'v (m/s)';}} function frame(now){{if(!running)return; if(last===null)last=now; clock+=((now-last)/1000)*parseFloat(speed.value);last=now;if(clock>=end){{clock=end;running=false;}}draw(clock);if(running)requestAnimationFrame(frame);}} play.onclick=()=>{{if(clock>=end)clock=0;running=true;last=null;requestAnimationFrame(frame);}};pause.onclick=()=>{{running=false;last=null;}};reset.onclick=()=>{{running=false;last=null;clock=0;draw(0);}};seek.oninput=()=>{{running=false;last=null;clock=(parseFloat(seek.value)||0)*end;draw(clock);}};chartSelect.onchange=()=>draw(clock);draw(0);}})();
    </script>
    """







