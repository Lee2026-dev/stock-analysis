# AI驱动的每日股票分析报告功能

## TL;DR

> **Quick Summary**: 为Alpha-X量化分析平台添加AI驱动的每日股票分析报告功能，结合技术指标和LLM新闻分析，生成涨跌原因分析和明日预测概率，并通过全新的专业金融终端UI展示。
> 
> **Deliverables**: 
> - 新闻数据获取模块（Akshare集成）
> - LLM智能分析引擎（OpenAI/Anthropic）
> - 报告生成协调器（技术面+消息面综合）
> - 报告存储系统（本地JSON）
> - 每日报告展示页面（专业金融风格UI）
> - 智能触发机制（16:00后自动检测生成）
> - UI全面升级（深色主题+中文化）
> 
> **Estimated Effort**: Large（预计15-20个任务）
> **Parallel Execution**: YES - 3个主要波次
> **Critical Path**: 数据层 → 逻辑层 → UI层 → 集成测试

---

## Context

### Original Request
用户希望为自选股每天交易结束后自动生成分析报告，包含：
1. 当日涨跌原因分析（技术面+消息面+资金面）
2. 明日涨跌概率预测（基于技术指标和政策分析）
3. 专业的报告展示界面

同时用户对当前UI不满意，认为过于简陋，尤其是侧边栏设计。

### Interview Summary

**Key Discussions**:
- **报告生成方式**: 混合模式（技术指标用规则引擎，新闻分析用LLM）
- **触发机制**: 智能检测式（用户16:00后打开应用自动生成，避免后台进程复杂度）
- **存储方式**: 本地JSON文件（`.sisyphus/reports/YYYYMMDD/{code}.json`）
- **UI风格**: 专业金融终端风格（Bloomberg/Wind inspired），深色主题，全中文

**Research Findings**:
- Akshare提供完整数据源（新闻、公告、财务、行情）
- pandas-ta最适合技术分析（纯Python，与Pandas原生集成）
- LLM成本可控（Top 5新闻过滤+GPT-4o-mini+缓存）
- Streamlit限制需要智能检测而非真后台调度

### Metis Review
**Identified Gaps** (自我审查):
- **LLM API Key管理**: 需要环境变量配置和错误处理
- **Akshare稳定性**: 需要回退策略（个股新闻→大盘新闻→纯技术分析）
- **首次生成等待时间**: 需要进度条和用户友好提示
- **报告历史**: 需要支持查看过往报告和准确率统计
- **UI CSS冲突**: Streamlit限制需要详细测试注入的CSS

---

## Work Objectives

### Core Objective
为自选股自动生成每日AI分析报告，结合量化技术指标和LLM新闻解读，预测下一交易日涨跌概率，并通过专业金融终端级UI呈现。

### Concrete Deliverables
- **数据层**: `src/data/news_fetcher.py` - 新闻/公告获取
- **AI层**: `src/logic/llm_agent.py` - LLM调用封装
- **分析层**: `src/logic/analyzer.py` - 技术面评分引擎
- **协调层**: `src/logic/report_engine.py` - 报告生成协调器
- **工具层**: `src/utils/cache.py` + `scheduler.py` - 缓存和触发逻辑
- **UI层**: `src/ui/reports.py` - 报告展示页面
- **UI升级**: `src/ui/styles.py` + `layout.py` - 深色主题+中文化
- **配置**: `pyproject.toml` - 新增依赖（openai, pandas-ta, python-dotenv）

### Definition of Done
- [ ] 16:00后打开应用自动生成所有自选股报告（带进度提示）
- [ ] 报告包含技术面、消息面、资金面分析和明日概率预测
- [ ] 报告页面UI达到专业金融终端水准（深色主题、中文标签、平滑交互）
- [ ] 侧边栏重新设计（实时行情卡片、折叠分组、悬浮效果）
- [ ] 所有用户可见文字为中文
- [ ] LLM调用失败时优雅降级（纯技术分析模式）
- [ ] 报告可查看历史和准确率统计

### Must Have
- 智能触发机制（交易日判断+时间检测+已生成检查）
- LLM成本控制（过滤、缓存、降级）
- 技术面规则引擎（基于RSI、MACD、MA等指标评分）
- 消息面LLM分析（情绪分类、影响评估）
- 明日概率计算（加权平均：技术60%+政策40%）
- 专业UI组件（评分条、概率仪表盘、行情卡片）

### Must NOT Have (Guardrails)
- ❌ **不使用独立后台进程**（避免部署复杂度，使用智能检测）
- ❌ **不修改现有核心逻辑**（indicators.py、backtest.py保持不变）
- ❌ **不依赖外部数据库**（使用本地JSON文件）
- ❌ **不使用外部JS框架**（限制在Streamlit能力内）
- ❌ **不破坏现有页面**（individual.py、market.py继续正常工作）
- ❌ **不过度调用LLM**（单只股票单日最多1次调用，严格缓存）
- ❌ **不添加英文标签**（所有用户可见文字必须中文）

---

## Verification Strategy

> **UNIVERSAL RULE: ZERO HUMAN INTERVENTION**
>
> ALL tasks in this plan MUST be verifiable WITHOUT any human action.

### Test Decision
- **Infrastructure exists**: NO（无现有测试基础设施）
- **Automated tests**: Tests-after（实现后补充单元测试）
- **Framework**: pytest（已在依赖中）

### Agent-Executed QA Scenarios (MANDATORY — ALL tasks)

每个任务必须包含Agent可执行的QA场景：
- **数据获取类**: 运行Python脚本获取数据，检查返回DataFrame非空
- **LLM类**: Mock API响应，验证解析逻辑正确
- **UI类**: 启动Streamlit，使用playwright验证元素渲染
- **集成类**: 完整流程测试（生成报告→读取文件→UI显示）

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - 可并行):
├── Task 1: 新增依赖到pyproject.toml
├── Task 2: 创建环境变量配置模板
├── Task 3: 实现news_fetcher.py（新闻数据获取）
├── Task 4: 实现llm_agent.py（LLM调用封装）
└── Task 5: 实现cache.py（报告缓存工具）

Wave 2 (After Wave 1 - 部分并行):
├── Task 6: 实现analyzer.py（技术面评分引擎）[depends: 1]
├── Task 7: 实现scheduler.py（触发逻辑）[depends: 5]
├── Task 8: 实现report_engine.py（报告协调器）[depends: 3,4,6]
├── Task 9: 更新styles.py（深色主题CSS）[depends: 1]
└── Task 10: 更新layout.py（侧边栏重设计）[depends: 9]

Wave 3 (After Wave 2 - 串行为主):
├── Task 11: 创建reports.py（报告展示页面）[depends: 9,10]
├── Task 12: 集成到app.py（路由+触发）[depends: 7,8,11]
├── Task 13: 端到端测试（完整流程）[depends: 12]
└── Task 14: 补充单元测试[depends: 13]

Critical Path: Task 1 → Task 3 → Task 8 → Task 12 → Task 13
Parallel Speedup: ~35%（Wave 1中5个任务并行）
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 6,9 | 2,3,4,5 |
| 2 | None | 4 | 1,3,5 |
| 3 | None | 8 | 1,2,4,5 |
| 4 | 2 | 8 | 1,3,5 |
| 5 | None | 7,8 | 1,2,3,4 |
| 6 | 1 | 8 | 7,9,10 |
| 7 | 5 | 12 | 6,9,10 |
| 8 | 3,4,6 | 12 | 9,10 |
| 9 | 1 | 10,11 | 6,7,8 |
| 10 | 9 | 11 | 6,7,8 |
| 11 | 9,10 | 12 | None |
| 12 | 7,8,11 | 13 | None |
| 13 | 12 | 14 | None |
| 14 | 13 | None | None |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1-5 | category="quick" for 1,2,5; category="unspecified-low" for 3,4 |
| 2 | 6-10 | category="unspecified-high" for 6,8; category="visual-engineering" + skills=["frontend-ui-ux"] for 9,10 |
| 3 | 11-14 | category="visual-engineering" + skills=["frontend-ui-ux"] for 11; category="deep" for 12,13 |

---

## TODOs

### Wave 1 - 基础设施层（可并行）

- [x] 1. 新增项目依赖

  **What to do**:
  - 编辑`pyproject.toml`，在`dependencies`数组添加：
    - `openai>=1.0.0`（LLM集成）
    - `anthropic>=0.25.0`（备用LLM）
    - `python-dotenv>=1.0.0`（环境变量）
    - `pandas-ta>=0.3.14b`（技术分析）
  - 运行`uv pip install -e .`安装依赖

  **Must NOT do**:
  - 不修改现有依赖版本
  - 不添加非必要的库

  **Recommended Agent Profile**:
  - **Category**: `quick`（简单配置修改）
  - **Skills**: []
  - **Reason**: 纯文本编辑，无复杂逻辑

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2,3,4,5)
  - **Blocks**: Tasks 6, 9
  - **Blocked By**: None

  **References**:
  - `pyproject.toml:7-14` - 现有依赖列表格式

  **Acceptance Criteria**:
  - [ ] `pyproject.toml`包含所有4个新依赖
  - [ ] 运行`uv pip list | grep -E "openai|anthropic|dotenv|pandas-ta"`显示所有包已安装

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 依赖安装验证
    Tool: Bash
    Preconditions: 编辑后的pyproject.toml已保存
    Steps:
      1. cd /Users/wenli/Desktop/workspace/stock-analysis
      2. .venv/bin/python -c "import openai; import anthropic; import dotenv; import pandas_ta; print('All imports successful')"
      3. Assert: stdout contains "All imports successful"
      4. Assert: exit code 0
    Expected Result: 所有包可成功导入
    Evidence: Terminal output captured
  ```

  **Commit**: YES
  - Message: `feat(deps): add LLM and technical analysis dependencies`
  - Files: `pyproject.toml`
  - Pre-commit: `uv pip install -e .`

---

- [x] 2. 创建环境变量配置模板

  **What to do**:
  - 创建`.env.example`文件，包含：
    ```
    # LLM API配置
    OPENAI_API_KEY=your-openai-key-here
    ANTHROPIC_API_KEY=your-anthropic-key-here
    LLM_PROVIDER=openai  # openai | anthropic
    
    # 报告生成配置
    MAX_NEWS_PER_STOCK=5
    REPORT_GEN_HOUR=16
    ```
  - 在README.md添加配置说明段落

  **Must NOT do**:
  - 不提交包含真实API Key的`.env`文件（添加到.gitignore）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 4
  - **Blocked By**: None

  **References**:
  - `.gitignore` - 确认`.env`已被忽略

  **Acceptance Criteria**:
  - [ ] `.env.example`文件存在且包含所有必要配置项
  - [ ] `.gitignore`包含`.env`条目
  - [ ] README.md包含配置说明

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 环境变量模板验证
    Tool: Bash
    Steps:
      1. cat .env.example
      2. Assert: 包含 "OPENAI_API_KEY"
      3. Assert: 包含 "ANTHROPIC_API_KEY"
      4. grep ".env" .gitignore
      5. Assert: exit code 0
    Expected Result: 模板完整且.env被忽略
    Evidence: cat和grep输出
  ```

  **Commit**: YES
  - Message: `chore(config): add environment variable template`
  - Files: `.env.example`, `README.md`, `.gitignore`

---

- [x] 3. 实现新闻数据获取模块（news_fetcher.py）

  **What to do**:
  - 创建`src/data/news_fetcher.py`
  - 实现`fetch_stock_news(symbol: str, limit: int = 5) -> pd.DataFrame`
    - 调用`ak.stock_news_em(symbol=symbol)`获取个股新闻
    - 若失败或返回空，回退到`ak.stock_news_jrj()`获取大盘新闻
    - 返回DataFrame，列：`['日期', '标题', '内容', '来源']`
    - 限制返回最新`limit`条
  - 实现`fetch_stock_announcements(symbol: str, limit: int = 3) -> pd.DataFrame`
    - 调用`ak.stock_announcement_em(symbol=symbol)`
    - 返回最新公告
  - 添加`@st.cache_data(ttl=3600)`缓存（1小时）

  **Must NOT do**:
  - 不做复杂的NLP预处理（交给LLM）
  - 不超过API调用限制（Akshare免费）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
  - **Skills**: []
  - **Reason**: 简单数据获取逻辑，参考现有fetcher.py模式

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 8
  - **Blocked By**: None

  **References**:
  - `src/data/fetcher.py:40-68` - 现有数据获取模式（缓存、异常处理）
  - Librarian研究结果 - `ak.stock_news_em(symbol=symbol)`用法

  **Acceptance Criteria**:
  - [ ] `src/data/news_fetcher.py`文件存在
  - [ ] 包含`fetch_stock_news`和`fetch_stock_announcements`函数
  - [ ] 运行`fetch_stock_news("000001")`返回非空DataFrame或优雅回退

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 获取个股新闻成功
    Tool: Bash
    Preconditions: Akshare可访问
    Steps:
      1. cd /Users/wenli/Desktop/workspace/stock-analysis
      2. .venv/bin/python -c "
         from src.data.news_fetcher import fetch_stock_news
         df = fetch_stock_news('000001', limit=3)
         assert not df.empty, 'News DataFrame is empty'
         assert '标题' in df.columns, 'Missing column'
         print(f'Fetched {len(df)} news items')
         print(df.head())
         "
      3. Assert: stdout contains "Fetched"
      4. Assert: exit code 0
    Expected Result: 成功获取新闻数据
    Evidence: DataFrame输出

  Scenario: Akshare失败时回退
    Tool: Bash (Mock)
    Steps:
      1. Mock ak.stock_news_em() raise Exception
      2. Call fetch_stock_news("999999")  # 无效代码
      3. Assert: 函数返回大盘新闻或空DataFrame，不抛异常
    Expected Result: 优雅降级，无崩溃
    Evidence: 无异常抛出
  ```

  **Commit**: YES
  - Message: `feat(data): add news fetcher with fallback strategy`
  - Files: `src/data/news_fetcher.py`
  - Pre-commit: `.venv/bin/python -m py_compile src/data/news_fetcher.py`

---

- [x] 4. 实现LLM调用封装（llm_agent.py）

  **What to do**:
  - 创建`src/logic/llm_agent.py`
  - 实现`analyze_news_sentiment(news_list: List[Dict], stock_name: str) -> Dict`
    - 输入：新闻列表（标题+内容前200字）+ 股票名称
    - 提示词模板：
      ```python
      PROMPT = f"""
      角色：资深A股分析师
      任务：分析以下新闻对{stock_name}的影响
      
      新闻数据：
      {json.dumps(news_list, ensure_ascii=False)}
      
      请输出JSON格式：
      {{
        "sentiment_score": 0-100,  // 0=极度悲观, 100=极度乐观
        "key_catalysts": ["利好1", "利好2"],
        "risk_warnings": ["风险1"],
        "summary": "100字以内的总结"
      }}
      """
      ```
    - 调用OpenAI/Anthropic API，解析JSON响应
    - 异常处理：API失败时返回默认值`{"sentiment_score": 50, "summary": "无消息面数据"}`
  - 使用`python-dotenv`加载API Key
  - 添加重试机制（最多3次）

  **Must NOT do**:
  - 不在代码中硬编码API Key
  - 不超过单次调用token限制（<2000 tokens）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
  - **Skills**: []
  - **Reason**: LLM调用封装，标准模式

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 8
  - **Blocked By**: Task 2

  **References**:
  - Task 2 - `.env`配置结构
  - Librarian研究结果 - LLM prompt模式

  **Acceptance Criteria**:
  - [ ] `src/logic/llm_agent.py`存在
  - [ ] `analyze_news_sentiment`函数正确返回结构化数据
  - [ ] API失败时优雅降级（返回默认值）

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Mock LLM响应解析
    Tool: Bash (Unit Test)
    Steps:
      1. cd /Users/wenli/Desktop/workspace/stock-analysis
      2. .venv/bin/python -c "
         import json
         from src.logic.llm_agent import analyze_news_sentiment
         # Mock响应（测试时不调用真实API）
         mock_news = [{'标题': '测试新闻', '内容': '测试内容'}]
         result = analyze_news_sentiment(mock_news, '平安银行')
         assert 'sentiment_score' in result
         assert 0 <= result['sentiment_score'] <= 100
         print('✅ LLM agent test passed')
         "
      3. Assert: stdout contains "passed"
    Expected Result: 返回结构正确
    Evidence: Test output

  Scenario: API Key缺失时降级
    Tool: Bash
    Steps:
      1. unset OPENAI_API_KEY
      2. Call analyze_news_sentiment([], "test")
      3. Assert: 返回 {"sentiment_score": 50, "summary": "无消息面数据"}
    Expected Result: 优雅降级
    Evidence: 返回默认值
  ```

  **Commit**: YES
  - Message: `feat(logic): add LLM agent with retry and fallback`
  - Files: `src/logic/llm_agent.py`

---

- [x] 5. 实现报告缓存工具（cache.py）

  **What to do**:
  - 创建`src/utils/cache.py`
  - 实现`get_report_path(date: str, stock_code: str) -> str`
    - 返回`.sisyphus/reports/YYYYMMDD/{stock_code}.json`
  - 实现`save_report(report: Dict, date: str, stock_code: str)`
    - 保存JSON到文件（自动创建目录）
  - 实现`load_report(date: str, stock_code: str) -> Optional[Dict]`
    - 读取JSON，不存在返回None
  - 实现`report_exists(date: str, stock_code: str) -> bool`
    - 检查文件是否存在

  **Must NOT do**:
  - 不使用数据库
  - 不缓存原始数据（只缓存最终报告）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 7, 8
  - **Blocked By**: None

  **References**:
  - 标准Python json模块和pathlib

  **Acceptance Criteria**:
  - [ ] `src/utils/cache.py`存在
  - [ ] 运行`save_report`后可用`load_report`读取
  - [ ] 目录`.sisyphus/reports/`自动创建

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 保存和读取报告
    Tool: Bash
    Steps:
      1. .venv/bin/python -c "
         from src.utils.cache import save_report, load_report
         test_report = {'score': 67, 'summary': 'test'}
         save_report(test_report, '20260204', '000001')
         loaded = load_report('20260204', '000001')
         assert loaded['score'] == 67
         print('✅ Cache test passed')
         "
      2. Assert: stdout contains "passed"
      3. ls .sisyphus/reports/20260204/000001.json
      4. Assert: file exists
    Expected Result: 缓存读写正常
    Evidence: File存在且内容正确
  ```

  **Commit**: YES
  - Message: `feat(utils): add report caching utilities`
  - Files: `src/utils/cache.py`

---

### Wave 2 - 核心逻辑层（部分并行）

- [x] 6. 实现技术面评分引擎（analyzer.py）

  **What to do**:
  - 创建`src/logic/analyzer.py`
  - 实现`calculate_technical_score(df: pd.DataFrame) -> Dict`
    - 输入：包含技术指标的DataFrame（来自`calculate_indicators`）
    - 评分规则（0-100分）：
      ```python
      score = 0
      # MA金叉/死叉 (+20/-20)
      if df.iloc[-1]['MA5'] > df.iloc[-1]['MA20']: score += 20
      # MACD柱状图正负 (+15/-15)
      if df.iloc[-1]['MACD_HIST'] > 0: score += 15
      # RSI超买超卖 (30-70正常+20, <30超卖+5, >70超买-10)
      rsi = df.iloc[-1]['RSI']
      if 30 < rsi < 70: score += 20
      elif rsi < 30: score += 5
      else: score -= 10
      # 布林带位置 (+10/-10)
      if df.iloc[-1]['收盘'] > df.iloc[-1]['BOLL_LOWER']: score += 10
      # 成交量放大 (+10)
      if df.iloc[-1]['成交量'] > df['成交量'].rolling(5).mean().iloc[-1]: score += 10
      ```
    - 返回`{"score": 0-100, "signals": ["MA5金叉MA20", ...]}`
  
  **Must NOT do**:
  - 不修改indicators.py
  - 不添加新的指标计算

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - **Reason**: 需要理解技术指标含义，设计评分逻辑

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with 7,9,10)
  - **Blocks**: Task 8
  - **Blocked By**: Task 1

  **References**:
  - `src/logic/indicators.py:5-89` - 技术指标计算逻辑
  - 现有backtest.py中的MA策略

  **Acceptance Criteria**:
  - [ ] `src/logic/analyzer.py`存在
  - [ ] `calculate_technical_score`返回0-100分数
  - [ ] 包含信号列表（如"MA5金叉MA20"）

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 评分逻辑验证
    Tool: Bash
    Steps:
      1. .venv/bin/python -c "
         import pandas as pd
         from src.data.fetcher import fetch_daily_history
         from src.logic.indicators import calculate_indicators
         from src.logic.analyzer import calculate_technical_score
         df = fetch_daily_history('000001', '20250101', '20260204')
         df = calculate_indicators(df)
         result = calculate_technical_score(df)
         assert 'score' in result
         assert 0 <= result['score'] <= 100
         assert 'signals' in result
         print(f'Score: {result[\"score\"]}')
         print(f'Signals: {result[\"signals\"]}')
         "
      2. Assert: stdout contains "Score:"
    Expected Result: 评分合理（0-100）
    Evidence: 评分输出
  ```

  **Commit**: YES
  - Message: `feat(logic): add technical scoring engine`
  - Files: `src/logic/analyzer.py`

---

- [x] 7. 实现智能触发逻辑（scheduler.py）

  **What to do**:
  - 创建`src/utils/scheduler.py`
  - 实现`is_trading_day(date: datetime.date = None) -> bool`
    - 判断是否为A股交易日（排除周末和节假日）
    - 可使用`akshare.tool_trade_date_hist_sina()`获取交易日历
  - 实现`should_generate_report() -> bool`
    - 检查：`is_trading_day() and datetime.now().hour >= 16 and not all_reports_exist_today()`
  - 实现`all_reports_exist_today() -> bool`
    - 遍历自选股，检查今日报告是否都已存在

  **Must NOT do**:
  - 不使用cron或APScheduler（保持简单）
  - 不硬编码节假日（使用Akshare API）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 12
  - **Blocked By**: Task 5

  **References**:
  - `src/utils/cache.py` - `report_exists`函数

  **Acceptance Criteria**:
  - [ ] `src/utils/scheduler.py`存在
  - [ ] `should_generate_report()`在16:00后交易日返回True（首次）
  - [ ] 重复调用返回False（已生成）

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 交易日判断
    Tool: Bash
    Steps:
      1. .venv/bin/python -c "
         from src.utils.scheduler import is_trading_day
         from datetime import date
         # 测试已知交易日
         result = is_trading_day(date(2026, 2, 4))  # 周三
         print(f'2026-02-04 is trading day: {result}')
         # 测试周末
         result_weekend = is_trading_day(date(2026, 2, 7))  # 周六
         assert result_weekend == False
         "
      2. Assert: 周六返回False
    Expected Result: 交易日判断准确
    Evidence: 输出结果
  ```

  **Commit**: YES
  - Message: `feat(utils): add smart trigger scheduler`
  - Files: `src/utils/scheduler.py`

---

- [x] 8. 实现报告生成协调器（report_engine.py）

  **What to do**:
  - 创建`src/logic/report_engine.py`
  - 实现`generate_report_for_stock(stock_code: str, date: str) -> Dict`
    - 步骤：
      1. 获取价格数据（`fetch_daily_history`）
      2. 计算技术指标（`calculate_indicators`）
      3. 计算技术面评分（`calculate_technical_score`）
      4. 获取新闻数据（`fetch_stock_news`）
      5. LLM分析新闻（`analyze_news_sentiment`）
      6. 获取资金流向（`fetch_northbound_flow`）
      7. 综合计算明日概率：`up_prob = tech_score * 0.6 + sentiment_score * 0.4`
      8. 组装报告JSON
    - 返回完整报告Dict
  - 实现`generate_all_reports(watchlist: List[str]) -> None`
    - 遍历自选股调用`generate_report_for_stock`
    - 显示Streamlit进度条
    - 保存到缓存

  **Must NOT do**:
  - 不并行生成（Streamlit限制，串行即可）
  - 不在LLM失败时中断（降级到纯技术分析）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - **Reason**: 核心协调逻辑，需要整合多个模块

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: N/A
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 3,4,6

  **References**:
  - `src/data/fetcher.py` - 数据获取模式
  - `src/logic/indicators.py` - 指标计算
  - `src/logic/analyzer.py` - 技术评分
  - `src/logic/llm_agent.py` - LLM分析
  - `src/utils/cache.py` - 报告保存

  **Acceptance Criteria**:
  - [ ] `src/logic/report_engine.py`存在
  - [ ] `generate_report_for_stock`返回完整报告结构
  - [ ] `generate_all_reports`可批量生成并保存

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 单只股票报告生成
    Tool: Bash
    Steps:
      1. .venv/bin/python -c "
         from src.logic.report_engine import generate_report_for_stock
         report = generate_report_for_stock('000001', '20260204')
         assert 'technical_analysis' in report
         assert 'news_analysis' in report
         assert 'prediction' in report
         assert 'up_probability' in report['prediction']
         print(f'Prediction: {report[\"prediction\"][\"up_probability\"]}%')
         "
      2. Assert: stdout contains "Prediction:"
      3. Assert: 概率在0-100之间
    Expected Result: 报告生成成功
    Evidence: 报告JSON结构完整
  ```

  **Commit**: YES
  - Message: `feat(logic): add report generation orchestrator`
  - Files: `src/logic/report_engine.py`

---

- [x] 9. 更新CSS样式（styles.py）

  **What to do**:
  - 修改`src/ui/styles.py`
  - 替换`inject_custom_css()`中的CSS为新设计：
    - 深色主题配色（变量：`--bg-primary: #0a0e27`, `--accent-primary: #00d4ff`等）
    - Sidebar样式（深色渐变背景、行情卡片、导航激活指示器）
    - 报告卡片样式（评分条、概率仪表盘、渐变背景）
    - 按钮、输入框、指标卡深色适配
  - 参考《UI/UX设计规范》中的完整CSS

  **Must NOT do**:
  - 不破坏现有页面布局（individual, market仍可用）
  - 不使用外部CSS文件（Streamlit限制）

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - **Reason**: UI样式重设计

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 10, 11
  - **Blocked By**: Task 1

  **References**:
  - 当前`src/ui/styles.py` - 现有CSS结构
  - 《UI/UX设计规范》- 新CSS代码

  **Acceptance Criteria**:
  - [ ] `inject_custom_css()`包含深色主题CSS
  - [ ] Sidebar背景为深色渐变
  - [ ] 新增评分条、仪表盘等组件样式

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: CSS语法验证
    Tool: Bash
    Steps:
      1. .venv/bin/python -c "
         from src.ui.styles import inject_custom_css
         # 运行函数不应报错
         inject_custom_css()
         print('✅ CSS injection successful')
         "
      2. Assert: stdout contains "successful"
    Expected Result: 无语法错误
    Evidence: 成功执行
  ```

  **Commit**: YES
  - Message: `feat(ui): apply professional dark theme styling`
  - Files: `src/ui/styles.py`

---

- [x] 10. 重设计侧边栏（layout.py）

  **What to do**:
  - 修改`src/ui/layout.py`
  - 更新`render_sidebar()`：
    - Logo区改为"🚀 盈立方 ALPHA-X | 专业量化分析系统"
    - 导航改为："🏠 工作台"、"📊 个股分析"、"📈 市场概览"、"📋 每日报告（新功能徽章）"
    - 自选股卡片改为实时行情卡片（显示涨跌、价格、成交量）
    - 添加"➕ 添加股票"按钮
    - 设置区折叠化
  - 实现`render_watchlist_card(stock_code)`函数
    - 获取实时行情（可用`ak.stock_zh_a_spot_em()`或缓存当日数据）
    - 渲染HTML卡片（包含涨跌颜色、图标）
  - 所有标签改为中文

  **Must NOT do**:
  - 不修改现有功能（自选股管理逻辑保持）
  - 不使用外部JS

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`

  **Parallelization**:
  - **Can Run In Parallel**: NO（依赖Task 9 CSS）
  - **Blocks**: Task 11
  - **Blocked By**: Task 9

  **References**:
  - 当前`src/ui/layout.py:18-80` - 现有侧边栏逻辑
  - 《UI/UX设计规范》- HTML/CSS示例

  **Acceptance Criteria**:
  - [ ] Sidebar显示"盈立方 ALPHA-X"品牌
  - [ ] 导航为中文（工作台、个股分析、市场概览、每日报告）
  - [ ] 自选股显示为行情卡片（涨跌、价格、成交量）

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 侧边栏渲染验证（需Playwright）
    Tool: Playwright (playwright skill)
    Steps:
      1. Start: streamlit run app.py (background)
      2. Navigate: http://localhost:8501
      3. Wait for: [data-testid="stSidebar"] visible
      4. Assert: text contains "盈立方 ALPHA-X"
      5. Assert: button contains "每日报告"
      6. Screenshot: .sisyphus/evidence/sidebar-redesign.png
    Expected Result: 侧边栏显示新设计
    Evidence: Screenshot
  ```

  **Commit**: YES
  - Message: `feat(ui): redesign sidebar with real-time stock cards`
  - Files: `src/ui/layout.py`

---

### Wave 3 - UI展示层（串行为主）

- [x] 11. 创建每日报告页面（reports.py）

  **What to do**:
  - 创建`src/ui/reports.py`
  - 实现`render_daily_reports()`函数：
    - 页面标题：" 📋 每日分析报告 | 2026年2月4日（今天）"
    - 显示统计：已分析X只股票、更新时间
    - "🔄 重新生成"按钮（调用`generate_all_reports`）
    - 遍历自选股，显示报告卡片（`render_report_card`）
  - 实现`render_report_card(stock_code, report: Dict)`：
    - 显示股票代码、名称、今日涨跌
    - 综合评分条（0-100，带颜色）
    - 分析摘要（技术面、消息面、资金面各一句）
    - 明日预测概率仪表盘（上涨XX% | 下跌XX%）
    - "查看完整报告 →"按钮（展开详情）
  - 实现`render_full_report(stock_code, report: Dict)`（详情视图）：
    - 分段显示：市场表现、技术分析、资金流向、消息面、明日预测、历史准确率
  - 所有文字中文化

  **Must NOT do**:
  - 不修改其他页面
  - 不使用React等外部框架

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 9, 10

  **References**:
  - `src/ui/individual.py` - 现有页面结构
  - `src/ui/components.py` - 组件渲染模式
  - 《UI/UX设计规范》- 报告页面mockup

  **Acceptance Criteria**:
  - [ ] `src/ui/reports.py`存在
  - [ ] 包含列表视图和详情视图
  - [ ] 显示评分条、概率仪表盘等可视化组件
  - [ ] 所有标签为中文

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 报告页面渲染（需Playwright）
    Tool: Playwright
    Steps:
      1. Generate mock report via cache.save_report()
      2. Start streamlit app
      3. Navigate to 报告页面
      4. Assert: 报告卡片存在
      5. Assert: 包含 "综合评分"
      6. Assert: 包含 "明日预测"
      7. Click "查看完整报告"
      8. Assert: 详情视图展开
      9. Screenshot: .sisyphus/evidence/report-page.png
    Expected Result: 页面完整渲染
    Evidence: Screenshot
  ```

  **Commit**: YES
  - Message: `feat(ui): add daily report display page`
  - Files: `src/ui/reports.py`

---

- [x] 12. 集成到主应用（app.py）

  **What to do**:
  - 修改`app.py`
  - 在路由部分添加"每日报告"分支：
    ```python
    if "每日报告" in page:
        # 智能触发检测
        if should_generate_report():
            with st.spinner("正在生成今日报告，预计需要60秒..."):
                generate_all_reports(user_inputs["watchlist"])
        
        render_daily_reports()
    ```
  - 确保`should_generate_report()`在应用启动时检测
  - 首次生成时显示进度条

  **Must NOT do**:
  - 不破坏现有路由
  - 不阻塞应用启动（检测快速完成）

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []
  - **Reason**: 核心集成逻辑，需理解整体流程

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Task 13
  - **Blocked By**: Tasks 7, 8, 11

  **References**:
  - 当前`app.py:34-42` - 路由逻辑
  - `src/utils/scheduler.py` - 触发检测
  - `src/logic/report_engine.py` - 报告生成

  **Acceptance Criteria**:
  - [ ] 侧边栏选择"每日报告"时正确路由
  - [ ] 16:00后首次打开自动生成（带进度提示）
  - [ ] 已生成时直接显示（不重复生成）

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 端到端流程测试
    Tool: Interactive Bash (tmux) + Playwright
    Steps:
      1. 清空今日报告缓存
      2. Mock时间为16:05
      3. tmux new-session: streamlit run app.py
      4. Playwright navigate to localhost:8501
      5. Click sidebar "每日报告"
      6. Assert: 显示进度条 "正在生成"
      7. Wait for: 进度完成（max 120s）
      8. Assert: 报告卡片显示
      9. Re-click "每日报告"
      10. Assert: 无重新生成（直接显示）
    Expected Result: 自动生成逻辑正确
    Evidence: Playwright screenshots + 缓存文件存在
  ```

  **Commit**: YES
  - Message: `feat(app): integrate daily report with smart trigger`
  - Files: `app.py`

---

- [x] 13. 端到端集成测试

  **What to do**:
  - 完整测试流程：
    1. 清空报告缓存
    2. 启动应用
    3. 验证16:00前不触发生成
    4. Mock时间到16:05
    5. 打开应用，验证自动生成
    6. 检查所有自选股报告已生成
    7. 验证UI显示正确（评分、预测、中文标签）
    8. 测试LLM降级（Mock API失败）
    9. 测试Akshare降级（Mock网络失败）
  - 记录所有测试结果

  **Must NOT do**:
  - 不使用真实API Key测试（使用Mock）

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Task 14
  - **Blocked By**: Task 12

  **References**:
  - 所有之前任务的QA场景

  **Acceptance Criteria**:
  - [ ] 所有核心流程通过测试
  - [ ] 降级场景无崩溃
  - [ ] UI渲染无CSS冲突

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 完整流程验证
    Tool: Playwright + Bash
    Steps:
      1. Setup: 清空缓存、设置Mock时间16:05
      2. Start: streamlit run app.py
      3. Navigate: localhost:8501
      4. Click: "每日报告"
      5. Wait: 进度条完成
      6. Assert: 3只股票报告卡片显示
      7. Click: 第一只股票"查看完整报告"
      8. Assert: 详情包含"技术分析"、"消息面"、"明日预测"
      9. Assert: 所有标签为中文
      10. Check files: .sisyphus/reports/20260204/*.json (3个文件)
    Expected Result: 全流程无错误
    Evidence: Screenshots + 缓存文件
  ```

  **Commit**: YES
  - Message: `test: add end-to-end integration tests`
  - Files: `tests/test_integration.py`（新增）

---

- [x] 14. 补充单元测试

  **What to do**:
  - 为核心模块添加pytest单元测试：
    - `tests/test_news_fetcher.py` - Mock Akshare API
    - `tests/test_llm_agent.py` - Mock OpenAI API
    - `tests/test_analyzer.py` - 技术评分逻辑
    - `tests/test_cache.py` - 文件读写
    - `tests/test_scheduler.py` - 交易日判断
  - 运行`pytest`确保全部通过

  **Must NOT do**:
  - 不依赖真实API（全部Mock）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: None（最终任务）
  - **Blocked By**: Task 13

  **References**:
  - 现有`tests/test_data.py` - 测试模式

  **Acceptance Criteria**:
  - [ ] `pytest`运行全部通过
  - [ ] 覆盖关键逻辑模块

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: 单元测试执行
    Tool: Bash
    Steps:
      1. cd /Users/wenli/Desktop/workspace/stock-analysis
      2. .venv/bin/python -m pytest tests/ -v
      3. Assert: exit code 0
      4. Assert: stdout contains "passed"
    Expected Result: 所有测试通过
    Evidence: pytest输出
  ```

  **Commit**: YES
  - Message: `test: add unit tests for core modules`
  - Files: `tests/test_*.py`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `feat(deps): add LLM and technical analysis dependencies` | pyproject.toml | uv pip install |
| 2 | `chore(config): add environment variable template` | .env.example, README.md | cat .env.example |
| 3 | `feat(data): add news fetcher with fallback strategy` | src/data/news_fetcher.py | pytest |
| 4 | `feat(logic): add LLM agent with retry and fallback` | src/logic/llm_agent.py | unit test |
| 5 | `feat(utils): add report caching utilities` | src/utils/cache.py | cache test |
| 6 | `feat(logic): add technical scoring engine` | src/logic/analyzer.py | pytest |
| 7 | `feat(utils): add smart trigger scheduler` | src/utils/scheduler.py | scheduler test |
| 8 | `feat(logic): add report generation orchestrator` | src/logic/report_engine.py | integration test |
| 9 | `feat(ui): apply professional dark theme styling` | src/ui/styles.py | CSS injection test |
| 10 | `feat(ui): redesign sidebar with real-time stock cards` | src/ui/layout.py | Playwright |
| 11 | `feat(ui): add daily report display page` | src/ui/reports.py | Playwright |
| 12 | `feat(app): integrate daily report with smart trigger` | app.py | E2E test |
| 13 | `test: add end-to-end integration tests` | tests/test_integration.py | pytest |
| 14 | `test: add unit tests for core modules` | tests/ | pytest |

---

## Success Criteria

### Verification Commands
```bash
# 1. 依赖安装验证
uv pip list | grep -E "openai|anthropic|pandas-ta"

# 2. 单元测试通过
pytest tests/ -v

# 3. 报告生成测试（Mock时间16:05）
python -c "from src.logic.report_engine import generate_all_reports; generate_all_reports(['000001'])"

# 4. 缓存文件检查
ls .sisyphus/reports/20260204/*.json

# 5. UI启动测试
streamlit run app.py  # 手动验证UI
```

### Final Checklist
- [ ] 所有"Must Have"功能已实现
- [ ] 所有"Must NOT Have"红线未触碰
- [ ] 所有测试通过（单元+集成）
- [ ] UI达到专业金融终端水准
- [ ] 所有用户可见文字为中文
- [ ] LLM成本可控（缓存+降级）
- [ ] 16:00后自动生成工作正常
