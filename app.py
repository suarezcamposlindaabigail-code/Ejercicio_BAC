"""
BAC SSC — Operaciones SWIFT
Asignación Óptima con Programación Entera Binaria
Curso II-1122 · UCR Alajuela
"""

import streamlit as st
import pandas as pd
import numpy as np
from itertools import permutations

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="BAC SSC · Operaciones SWIFT",
    page_icon="🏦",
    layout="wide",
)

# ── Estilos ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title  { color:#1a237e; font-size:2rem; font-weight:700; }
    .sub-title   { color:#b71c1c; font-size:1.1rem; margin-top:-10px; }
    .kpi-card    { background:#f5f5f5; border-left:5px solid #1a237e;
                   padding:12px 18px; border-radius:6px; margin-bottom:8px; }
    .kpi-label   { font-size:.8rem; color:#555; text-transform:uppercase;
                   letter-spacing:.05em; }
    .kpi-value   { font-size:1.6rem; font-weight:700; color:#1a237e; }
    .optimal-tag { background:#e8f5e9; color:#2e7d32; font-weight:600;
                   padding:4px 12px; border-radius:20px; display:inline-block; }
    .blocked     { background:#ffebee; color:#c62828; text-align:center;
                   border-radius:4px; padding:2px 6px; }
    .assigned    { background:#e3f2fd; color:#1565c0; font-weight:700;
                   text-align:center; border-radius:4px; padding:2px 6px; }
</style>
""", unsafe_allow_html=True)

# ── Datos del problema ───────────────────────────────────────────────────────
ANALISTAS   = ["Andrea (A)", "Beatriz (B)", "Carlos (C)", "Daniel (D)", "Esteban (E)"]
OPERACIONES = ["MT103", "MT202", "MT700", "MT760", "MT940"]
LABELS_OP   = {
    "MT103": "Transferencia cliente → Panamá",
    "MT202": "Transferencia interbancaria → Guatemala",
    "MT700": "Carta de crédito (LC) → Honduras",
    "MT760": "Garantía bancaria",
    "MT940": "Reporte de cuenta",
}

# Tiempos (minutos); None = bloqueado
INF = 999
TIEMPOS = {
    "A": {"MT103": 25, "MT202": 30, "MT700": INF, "MT760": INF, "MT940": 20},
    "B": {"MT103": 35, "MT202": 28, "MT700": 40, "MT760": 45, "MT940": 22},
    "C": {"MT103": 40, "MT202": 45, "MT700": 35, "MT760": 30, "MT940": 25},
    "D": {"MT103": 30, "MT202": 32, "MT700": 50, "MT760": INF, "MT940": 18},
    "E": {"MT103": INF, "MT202": INF, "MT700": 30, "MT760": 28, "MT940": 30},
}
KEYS = ["A", "B", "C", "D", "E"]   # orden para permutaciones

DISPONIBLE = {
    "A": {"MT103": 1, "MT202": 1, "MT700": 0, "MT760": 0, "MT940": 1},
    "B": {"MT103": 1, "MT202": 1, "MT700": 1, "MT760": 1, "MT940": 1},
    "C": {"MT103": 1, "MT202": 1, "MT700": 1, "MT760": 1, "MT940": 1},
    "D": {"MT103": 1, "MT202": 1, "MT700": 1, "MT760": 0, "MT940": 1},
    "E": {"MT103": 0, "MT202": 0, "MT700": 1, "MT760": 1, "MT940": 1},
}

# ── Solver por fuerza bruta (5! = 120 permutaciones) ────────────────────────
def resolver():
    ops = OPERACIONES[:]
    best_time = float("inf")
    best_perm = None
    feasible_count = 0
    all_solutions = []

    for perm in permutations(KEYS):
        asignacion = dict(zip(ops, perm))   # op → analista_key
        # Verificar compliance
        if any(DISPONIBLE[a][op] == 0 for op, a in asignacion.items()):
            continue
        feasible_count += 1
        total = sum(TIEMPOS[a][op] for op, a in asignacion.items())
        all_solutions.append((total, dict(asignacion)))
        if total < best_time:
            best_time = total
            best_perm = dict(asignacion)

    all_solutions.sort(key=lambda x: x[0])
    return best_perm, best_time, feasible_count, all_solutions[:10]


# ── Layout ───────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🏦 BAC SSC — Operaciones SWIFT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Asignación Óptima · Programación Entera Binaria · II-1122 UCR</div>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Datos del Problema",
    "⚙️ Resolución",
    "📊 Análisis de Sensibilidad",
    "📁 Archivos AMPL"
])

# ════════════════════════════════════════════════════════════
# TAB 1 — Datos
# ════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Lote del día — 5 operaciones SWIFT urgentes (cierre 11:00 a.m.)")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### ⏱️ Matriz de tiempos (minutos)")
        df_t = pd.DataFrame(
            [[TIEMPOS[k][op] if TIEMPOS[k][op] < INF else "🚫" for op in OPERACIONES]
             for k in KEYS],
            index=ANALISTAS,
            columns=OPERACIONES,
        )
        st.dataframe(df_t, use_container_width=True)

    with col2:
        st.markdown("#### 🔐 Compliance Bridger")
        df_d = pd.DataFrame(
            [["✅" if DISPONIBLE[k][op] else "🚫" for op in OPERACIONES]
             for k in KEYS],
            index=ANALISTAS,
            columns=OPERACIONES,
        )
        st.dataframe(df_d, use_container_width=True)

    st.info("""
    **Restricciones de compliance:**
    - **Andrea** no puede ejecutar MT700 (LC) ni MT760 (Garantía)
    - **Daniel** no puede ejecutar MT760 (Garantía)
    - **Esteban** no puede ejecutar MT103 ni MT202 (en re-certificación)
    """)

    st.markdown("#### 📌 Descripción de operaciones")
    for op, desc in LABELS_OP.items():
        st.markdown(f"- **{op}** — {desc}")


# ════════════════════════════════════════════════════════════
# TAB 2 — Resolución
# ════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Solución óptima")

    if st.button("▶️ Resolver ahora", type="primary"):
        best, best_time, n_feasible, top10 = resolver()

        # KPIs
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Tiempo total del lote</div>
                <div class="kpi-value">{best_time} min</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Soluciones factibles</div>
                <div class="kpi-value">{n_feasible}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Variables binarias</div>
                <div class="kpi-value">25</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### ✅ Asignación óptima")
        analista_nombre = dict(zip(KEYS, ANALISTAS))
        rows = []
        for op in OPERACIONES:
            a_key = best[op]
            rows.append({
                "Operación": op,
                "Descripción": LABELS_OP[op],
                "Analista asignado": analista_nombre[a_key],
                "Tiempo (min)": TIEMPOS[a_key][op],
            })
        df_sol = pd.DataFrame(rows)
        st.dataframe(df_sol, use_container_width=True, hide_index=True)

        st.success(f"🎯 **Tiempo total mínimo del lote: {best_time} minutos**")

        st.markdown("#### 🏆 Top 10 soluciones factibles")
        top_rows = []
        for rank, (t, asig) in enumerate(top10, 1):
            row = {"Rank": rank, "Tiempo total": t}
            for op in OPERACIONES:
                row[op] = analista_nombre[asig[op]]
            top_rows.append(row)
        st.dataframe(pd.DataFrame(top_rows), use_container_width=True, hide_index=True)

    else:
        st.info("Haz clic en **Resolver ahora** para ejecutar el modelo.")


# ════════════════════════════════════════════════════════════
# TAB 3 — Análisis de sensibilidad
# ════════════════════════════════════════════════════════════
with tab3:
    st.subheader("📊 Análisis de Sensibilidad")
    st.markdown("Explora cómo cambia la solución óptima al modificar tiempos individuales.")

    best_base, base_time, _, _ = resolver()
    analista_nombre = dict(zip(KEYS, ANALISTAS))

    st.markdown("#### 🔧 Simulador de escenarios")
    col_a, col_b = st.columns(2)
    with col_a:
        analista_sel = st.selectbox("Analista", ANALISTAS)
    with col_b:
        op_sel = st.selectbox("Operación", OPERACIONES)

    a_key = KEYS[ANALISTAS.index(analista_sel)]

    if DISPONIBLE[a_key][op_sel] == 0:
        st.warning("⛔ Esta celda está bloqueada por compliance — no se puede asignar.")
    else:
        tiempo_actual = TIEMPOS[a_key][op_sel]
        nuevo_tiempo = st.slider(
            f"Nuevo tiempo para {analista_sel} → {op_sel}",
            min_value=5, max_value=90, value=tiempo_actual, step=1
        )

        # Recalcular con el nuevo tiempo
        TIEMPOS_MOD = {k: dict(v) for k, v in TIEMPOS.items()}
        TIEMPOS_MOD[a_key][op_sel] = nuevo_tiempo

        def resolver_mod(tiempos_mod):
            ops = OPERACIONES[:]
            best_time_m = float("inf")
            best_perm_m = None
            for perm in permutations(KEYS):
                asig = dict(zip(ops, perm))
                if any(DISPONIBLE[a][op] == 0 for op, a in asig.items()):
                    continue
                total = sum(tiempos_mod[a][op] for op, a in asig.items())
                if total < best_time_m:
                    best_time_m = total
                    best_perm_m = dict(asig)
            return best_perm_m, best_time_m

        best_mod, time_mod = resolver_mod(TIEMPOS_MOD)
        delta = time_mod - base_time

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Tiempo base", f"{base_time} min")
        mc2.metric("Tiempo modificado", f"{time_mod} min", delta=f"{delta:+d} min",
                   delta_color="inverse")
        mc3.metric("Cambio %", f"{delta/base_time*100:+.1f}%")

        if best_mod != best_base:
            st.warning("⚠️ **La solución óptima cambia** con este ajuste.")
            rows_mod = []
            for op in OPERACIONES:
                a_k = best_mod[op]
                rows_mod.append({
                    "Operación": op,
                    "Analista": analista_nombre[a_k],
                    "Tiempo (min)": TIEMPOS_MOD[a_k][op],
                })
            st.dataframe(pd.DataFrame(rows_mod), use_container_width=True, hide_index=True)
        else:
            st.success("✅ La asignación óptima **no cambia** — la solución es robusta.")

    # Tabla de rangos
    st.markdown("---")
    st.markdown("#### 📋 Tabla de rangos de estabilidad (análisis ±10 min por celda)")
    rows_sens = []
    for k in KEYS:
        for op in OPERACIONES:
            if DISPONIBLE[k][op] == 0:
                continue
            t0 = TIEMPOS[k][op]
            # Buscar límite inferior y superior donde la solución no cambia
            estable = True
            for delta in range(-30, 31, 1):
                t_new = t0 + delta
                if t_new <= 0:
                    continue
                TIEMPOS_T = {kk: dict(vv) for kk, vv in TIEMPOS.items()}
                TIEMPOS_T[k][op] = t_new
                bp, _ = resolver_mod(TIEMPOS_T)
                if bp != best_base:
                    estable = False
                    break
            rows_sens.append({
                "Analista": analista_nombre[k],
                "Operación": op,
                "Tiempo base": t0,
                "¿Solución estable ±30 min?": "✅ Sí" if estable else "⚠️ No",
            })
    st.dataframe(pd.DataFrame(rows_sens), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# TAB 4 — Archivos AMPL
# ════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📁 Archivos AMPL para ejecutar en CBC")

    st.markdown("#### 📄 bac_swift.mod — Modelo simbólico")
    st.code(open("bac_swift.mod").read() if True else "", language="text")
    # Mostrar hardcoded para Streamlit Cloud
    st.code("""set ANALISTAS;
set OPERACIONES;

param tiempo{i in ANALISTAS, j in OPERACIONES} >= 0;
param disponible{i in ANALISTAS, j in OPERACIONES} binary;

var x{i in ANALISTAS, j in OPERACIONES} binary;

minimize Tiempo_total:
    sum{i in ANALISTAS, j in OPERACIONES} tiempo[i,j] * x[i,j];

s.t. Op{j in OPERACIONES}:
    sum{i in ANALISTAS} x[i,j] = 1;

s.t. An{i in ANALISTAS}:
    sum{j in OPERACIONES} x[i,j] = 1;

s.t. Comp{i in ANALISTAS, j in OPERACIONES}:
    x[i,j] <= disponible[i,j];""", language="text")

    st.markdown("#### 📄 bac_swift.dat — Datos")
    st.code("""set ANALISTAS  := A B C D E;
set OPERACIONES := MT103 MT202 MT700 MT760 MT940;

param tiempo :
           MT103  MT202  MT700  MT760  MT940 :=
  A          25     30    999    999     20
  B          35     28     40     45     22
  C          40     45     35     30     25
  D          30     32     50    999     18
  E         999    999     30     28     30 ;

param disponible :
           MT103  MT202  MT700  MT760  MT940 :=
  A          1      1      0      0      1
  B          1      1      1      1      1
  C          1      1      1      1      1
  D          1      1      1      0      1
  E          0      0      1      1      1 ;""", language="text")

    st.markdown("#### ⚡ Comando para ejecutar localmente")
    st.code("ampl bac_swift.mod bac_swift.dat", language="bash")

st.markdown("---")
st.caption("II-1122 · Programación Entera Mixta con Software · UCR Alajuela")
