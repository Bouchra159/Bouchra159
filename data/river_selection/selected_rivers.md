# Selected Study Rivers — GLORIN-Based Selection

## Selection Rationale

Rivers were selected from the **GLORIN (Global River Information)** dataset following criteria established with supervisors:
- Large rivers (mean annual discharge > 1,000 m³/s)
- Geographic diversity: multiple latitudes AND altitudes
- Representative of different climate regimes
- Availability of reference/validation data

The final selection of **8 rivers** covers 5 climate zones, 4 continents, and spans from near-equatorial to subarctic latitudes.

---

## River Profiles

### R01 — Amazon River (Manaus reach, Brazil)
- **Coordinates:** ~3.1°S, 60.0°W (near confluence with Rio Negro)
- **GLORIN ID:** TBD (verify in dataset)
- **Altitude:** ~40 m a.s.l.
- **Mean discharge:** ~120,000 m³/s (world's largest by discharge)
- **Width:** 2–10 km (main channel)
- **Climate:** Tropical Rainforest (Af)
- **Cloud cover:** >80% annually — strong SAR case
- **Flood seasonality:** Peak: May–June; Low: September–October
- **Key challenge:** Almost year-round cloud cover defeats optical; flooded forest complicates SAR
- **Validation:** JRC GSW; SWOT (post-2023)
- **Notes:** Highly dynamic floodplain; braided channels in some reaches

### R02 — Congo River (Kinshasa reach, DRC)
- **Coordinates:** ~4.3°S, 15.3°E
- **GLORIN ID:** TBD
- **Altitude:** ~280 m a.s.l.
- **Mean discharge:** ~41,000 m³/s (2nd largest by discharge)
- **Width:** 4–14 km (Pool Malebo upstream of Kinshasa)
- **Climate:** Tropical Wet-Dry (Aw)
- **Cloud cover:** >70% annually
- **Flood seasonality:** Bimodal — peaks November and May
- **Key challenge:** Cloud cover; rapids immediately downstream (Livingstone Falls)
- **Validation:** JRC GSW
- **Notes:** Unique bimodal discharge due to basin straddling equator

### R03 — Nile River (Luxor/Aswan reach, Egypt)
- **Coordinates:** ~25.7°N, 32.6°E
- **GLORIN ID:** TBD
- **Altitude:** ~80 m a.s.l.
- **Mean discharge:** ~2,800 m³/s (regulated by Aswan High Dam)
- **Width:** 0.5–1.5 km
- **Climate:** Desert (BWh)
- **Cloud cover:** <5% annually — strong optical case
- **Flood seasonality:** Regulated; minimal natural flooding post-dam
- **Key challenge:** Narrow width; irrigated agriculture flanking river; no natural flood
- **Validation:** JRC GSW; moderate field data
- **Notes:** Dam impact must be documented; Nile Delta not included

### R04 — Ganges River (Patna reach, India)
- **Coordinates:** ~25.6°N, 85.1°E
- **GLORIN ID:** TBD
- **Altitude:** ~55 m a.s.l.
- **Mean discharge:** ~12,000 m³/s (summer monsoon driven)
- **Width:** 1–5 km (extreme seasonal variability)
- **Climate:** Humid Subtropical / Tropical Monsoon (Cwa/Am)
- **Cloud cover:** ~60% during monsoon (June–September)
- **Flood seasonality:** Peak: July–August (monsoon); very low: March–May
- **Key challenge:** Cloud cover during flood peaks — SAR critical; high turbidity
- **Validation:** JRC GSW; some field surveys available
- **Notes:** Extreme seasonal width change is scientifically important

### R05 — Yangtze River (Wuhan reach, China)
- **Coordinates:** ~30.6°N, 114.3°E
- **GLORIN ID:** TBD
- **Altitude:** ~23 m a.s.l.
- **Mean discharge:** ~22,000 m³/s (3rd largest by discharge)
- **Width:** 1–3 km
- **Climate:** Humid Subtropical (Cfa)
- **Cloud cover:** ~50–60% during summer
- **Flood seasonality:** Peak: June–July; major flood events documented
- **Key challenge:** Turbid water (Yellow-brown sediment load); cloud during floods
- **Validation:** JRC GSW; 2020 flood event (well documented)
- **Notes:** Three Gorges Dam impact upstream; downstream reach selected

### R06 — Mississippi River (Memphis reach, USA)
- **Coordinates:** ~35.1°N, 90.0°W
- **GLORIN ID:** TBD
- **Altitude:** ~75 m a.s.l.
- **Mean discharge:** ~16,000 m³/s
- **Width:** 0.5–2 km
- **Climate:** Humid Subtropical (Cfa)
- **Cloud cover:** ~40–50%
- **Flood seasonality:** Peak: March–May (spring snowmelt)
- **Key challenge:** Moderate cloud cover; levee system restricts natural flooding
- **Validation:** JRC GSW; USGS stream gauges (excellent reference data)
- **Notes:** Best-documented large river; benchmark for method validation

### R07 — Rhine River (Cologne reach, Germany)
- **Coordinates:** ~50.9°N, 6.9°E
- **GLORIN ID:** TBD
- **Altitude:** ~37 m a.s.l.
- **Mean discharge:** ~2,300 m³/s
- **Width:** 0.2–0.4 km (relatively narrow)
- **Climate:** Oceanic (Cfb)
- **Cloud cover:** ~55–65% annually
- **Flood seasonality:** Peak: December–February (winter rain)
- **Key challenge:** Narrow width (sub-pixel at some resolutions); dense cloud cover
- **Validation:** JRC GSW; German BfG data (Bundesanstalt für Gewässerkunde)
- **Notes:** European benchmark; good institutional data availability

### R08 — Ob River (Salekhard reach, Russia)
- **Coordinates:** ~66.5°N, 66.6°E
- **GLORIN ID:** TBD
- **Altitude:** ~10 m a.s.l.
- **Mean discharge:** ~12,800 m³/s
- **Width:** 2–5 km (braided during spring)
- **Climate:** Subarctic (Dfc)
- **Cloud cover:** Variable; snow/ice cover Oct–May
- **Flood seasonality:** Spring ice breakup: May–June (dramatic)
- **Key challenge:** Ice cover; SAR signature of ice vs. water ambiguity; polar day/night
- **Validation:** JRC GSW
- **Notes:** Ice breakup flood mapping is unique scientific contribution; limited optical winter data

---

## Geographic Coverage

```
Climate Zone      Rivers              Latitude Range
─────────────────────────────────────────────────────
Tropical          Amazon, Congo       3°S – 4°S
Arid              Nile                25°N
Monsoon           Ganges              25°N
Humid Subtropical Yangtze, Miss.     30–35°N
Oceanic           Rhine               51°N
Subarctic         Ob                  66°N
```

Altitude range: 10 m (Ob delta) → 280 m (Congo, Kinshasa)

---

## Data Download Checklist

- [ ] R01 Amazon: S1 (2019–2024), S2 (2019–2024), JRC GSW
- [ ] R02 Congo: S1 (2019–2024), S2 (2019–2024), JRC GSW
- [ ] R03 Nile: S1 (2019–2024), S2 (2019–2024), JRC GSW
- [ ] R04 Ganges: S1 (2019–2024), S2 (2019–2024), JRC GSW
- [ ] R05 Yangtze: S1 (2019–2024), S2 (2019–2024), JRC GSW
- [ ] R06 Mississippi: S1 (2019–2024), S2 (2019–2024), JRC GSW, USGS gauge data
- [ ] R07 Rhine: S1 (2019–2024), S2 (2019–2024), JRC GSW
- [ ] R08 Ob: S1 (2019–2024), S2 (2019–2024, summer only), JRC GSW
