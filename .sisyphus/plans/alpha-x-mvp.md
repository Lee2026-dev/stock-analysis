# Work Plan: Alpha-X Stock Analysis MVP

## 1. Context & Objectives
- **Goal**: Build a production-grade B2B stock analysis SaaS MVP called "Alpha-X".
- **Target Audience**: Professional traders/institutions (B2B).
- **Core Value**: High-win rate signal simulation (Core Pool) + Real-time technical analysis (Long-tail).
- **Tech Stack**: Python 3.12+ (uv), Streamlit, Akshare, Pandas, Streamlit Lightweight Charts (TradingView).
- **Language**: Simplified Chinese (UI).

## 2. Technical Architecture
- **Structure**: Modular multi-file (NOT single-script).
  ```text
  alpha-x/
  ├── pyproject.toml       # Dependencies managed by uv
  ├── app.py               # Main Streamlit entry point
  ├── src/
  │   ├── data/            # Data ingestion (Akshare)
  │   ├── logic/           # Indicators, Backtesting, Win Rate
  │   ├── ui/              # Components, Layouts, CSS
  │   └── utils/           # Shared helpers
  └── tests/               # Unit tests
  ```
- **Data Strategy**: 
  - `akshare` with `adjust="qfq"` (forward adjusted).
  - Robust error handling: Return empty Schema-compliant DataFrame on timeout/failure.
  - Caching: `st.cache_data(ttl=60)` for hot data.
- **UI/UX Strategy**:
  - **SaaS Look**: Fixed container layouts (`st.container(height=...)`), "Card" styling via injected CSS.
  - **Charts**: `streamlit-lightweight-charts-v5` for professional financial viz.
  - **Colors**: Red=Up, Green=Down (China standard).

## 3. Phased Execution Plan

### Phase 1: Foundation & Data Layer
**Goal**: robust data ingestion with error handling.
- [ ] **Step 1.1**: Initialize project with `uv` (`pyproject.toml`) and install core deps (`streamlit`, `akshare`, `pandas`, `streamlit-lightweight-charts-v5`).
- [ ] **Step 1.2**: Create `src/data/fetcher.py`. Implement `fetch_daily_history` and `fetch_northbound_flow`.
  - *Requirement*: Handle `requests.Timeout` and `ConnectionError`. Return empty DF with correct columns on fail.
- [ ] **Step 1.3**: Create `tests/test_data.py`. Write unit tests for the fetcher (mocking `akshare` to test error paths).
- [ ] **Step 1.4**: Verify data fetching manually via a simple script.

### Phase 2: Logic Engine (Indicators & Backtest)
**Goal**: Transform raw data into signals and metrics.
- [ ] **Step 2.1**: Create `src/logic/indicators.py`. Implement calculation functions using Pandas:
  - Simple: MA5, MA20, Volume MA.
  - Complex: RSI, MACD, Bollinger Bands, KDJ, OBV.
- [ ] **Step 2.2**: Create `src/logic/backtest.py`.
  - *Logic*: Input (Stock Code, Date Range) → Output (Win Rate %, Total Return).
  - *Strategy*: Simple crossover strategy to generate the stats for the "Core Pool".
- [ ] **Step 2.3**: Create `tests/test_logic.py`. Verify indicator math against known values.

### Phase 3: UI Components & Layout
**Goal**: Build the "SaaS" shell and visual components.
- [ ] **Step 3.1**: Create `src/ui/styles.py`. Define CSS for "Card" UI, removing Streamlit branding, and typography.
- [ ] **Step 3.2**: Create `src/ui/components.py`.
  - `render_metric_card`: Custom HTML/CSS metric display (Red/Green logic).
  - `render_chart`: Wrapper for `streamlit-lightweight-charts-v5` configuration.
- [ ] **Step 3.3**: Implement the Main Layout in `src/ui/layout.py`.
  - Sidebar: Navigation (Market Overview, Individual Analysis), Stock Selector, Date Range.
  - Main Area: Grid system with `st.columns`.

### Phase 4: Integration & Application Logic
**Goal**: Connect data, logic, and UI.
- [ ] **Step 4.1**: Implement "Individual Analysis" Page.
  - Input: User selects code (default Core Pool or custom).
  - Action: Fetch data → Calc Indicators → Run Backtest (if Core) → Render Chart + Metrics.
- [ ] **Step 4.2**: Implement "Market Overview" Page.
  - Content: Northbound Fund Flow dashboard (Market aggregate + Top holdings).
- [ ] **Step 4.3**: Integrate Auto-refresh (Polling).
  - Use `st_autorefresh` or `st.rerun` logic (careful with API limits).

### Phase 5: Verification & Polish
**Goal**: Final QA and constraints check.
- [ ] **Step 5.1**: Run `pytest` suite. Ensure all critical paths pass.
- [ ] **Step 5.2**: Manual UX Polish.
  - Check Mobile responsiveness.
  - Verify "China Standard" colors (Red=Up) everywhere.
- [ ] **Step 5.3**: Clean up code. Add Type Annotations (`mypy` compatible) and Docstrings.

## 4. Guardrails & Constraints
- **NO** Authentication or User Management.
- **NO** Database persistence (in-memory/cache only).
- **NO** Docker/Deployment configuration (Code only).
- **Critical**: If `akshare` fails, the app must NOT crash. Show "Data Unavailable" toast.
- **Critical**: Win Rate simulation must feel "real" (derived from backtest logic, not random.random()).

## 5. Verification Checklist
- [ ] `uv run app.py` launches without errors.
- [ ] Entering an invalid stock code handles gracefully.
- [ ] Disconnecting internet and reloading shows error state, not stack trace.
- [ ] Charts are interactive and show correct Red/Green candles.
- [ ] Type hints present in all `src/` files.
