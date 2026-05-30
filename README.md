# 🏦 BAC SSC — Operaciones SWIFT
### Asignación Óptima con Programación Entera Binaria

**Curso II-1122 · Programación Entera Mixta con Software · UCR Alajuela**

---

## 📋 Descripción del problema

El Centro de Servicios Compartidos (SSC) de BAC Credomatic procesa cada mañana un lote de 5 operaciones SWIFT urgentes provenientes de Costa Rica, Guatemala, Honduras y Panamá.

Se deben asignar **5 operaciones a 5 analistas** (una cada uno) **minimizando el tiempo total de procesamiento del lote**, respetando restricciones de compliance Bridger.

| Operación | Descripción |
|-----------|-------------|
| MT103 | Transferencia cliente → Panamá |
| MT202 | Transferencia interbancaria → Guatemala |
| MT700 | Carta de crédito (LC) → Honduras |
| MT760 | Garantía bancaria |
| MT940 | Reporte de cuenta |

### Restricciones de compliance Bridger
- **Andrea** no puede ejecutar MT700 ni MT760
- **Daniel** no puede ejecutar MT760
- **Esteban** no puede ejecutar MT103 ni MT202 (en re-certificación)

---

## 🧮 Modelo matemático

**Variable de decisión:** xᵢⱼ ∈ {0,1} → 1 si analista *i* ejecuta operación *j*

**Función objetivo:**
```
Min Z = Σᵢ Σⱼ tiempo[i,j] · x[i,j]
```

**Restricciones:**
- Cada operación asignada a exactamente 1 analista
- Cada analista recibe exactamente 1 operación
- Celdas bloqueadas por compliance = 0

---

## 📁 Archivos del repositorio

| Archivo | Descripción |
|---------|-------------|
| `bac_swift.mod` | Modelo AMPL simbólico |
| `bac_swift.dat` | Datos del problema |
| `app.py` | App Streamlit con solver y análisis de sensibilidad |
| `requirements.txt` | Dependencias Python |

---

## 🚀 Cómo ejecutar

### Opción 1 — AMPL/CBC
```bash
ampl bac_swift.mod bac_swift.dat
```

### Opción 2 — Streamlit local
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Opción 3 — Streamlit Cloud
Subir el repositorio a GitHub y conectarlo en [share.streamlit.io](https://share.streamlit.io).

---

## 📊 Solución óptima esperada

| Analista | Operación | Tiempo |
|----------|-----------|--------|
| Andrea (A) | MT940 | 20 min |
| Beatriz (B) | MT202 | 28 min |
| Carlos (C) | MT760 | 30 min |
| Daniel (D) | MT103 | 30 min |
| Esteban (E) | MT700 | 30 min |
| **TOTAL** | | **138 min** |

---

*II-1122 · UCR Alajuela*
