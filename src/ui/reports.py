import streamlit as st
import datetime
from typing import Dict, Any, List
from src.utils.cache import load_report
from src.logic.report_engine import generate_all_reports


def render_score_bar(score: int):
    """
    Render a colorful score bar (0-100).
    """
    color = "#ef4444" if score < 40 else "#fbbf24" if score < 70 else "#10b981"

    html = f"""
    <div style="margin-top: 8px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 0.8em; color: #94a3b8;">综合评分</span>
            <span style="font-weight: bold; color: {color};">{score}/100</span>
        </div>
        <div class="score-bar-bg">
            <div class="score-bar-fill" style="width: {score}%; background: {color};"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_probability_gauge(up_prob: int):
    """
    Render a probability gauge.
    """
    down_prob = 100 - up_prob
    color = "#ef4444" if up_prob >= 50 else "#10b981"  # China: Red=Up

    st.markdown(
        f"""
        <div style="text-align: center; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.9em; color: #94a3b8;">明日上涨概率</div>
            <div style="font-size: 2em; font-weight: bold; color: {color}; margin: 5px 0;">{up_prob}%</div>
            <div style="display: flex; height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="width: {up_prob}%; background: #ef4444;" title="上涨"></div>
                <div style="width: {down_prob}%; background: #10b981;" title="下跌"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.7em; color: #64748b; margin-top: 4px;">
                <span>看涨 {up_prob}%</span>
                <span>看跌 {down_prob}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report_card(stock_code: str, report: Dict[str, Any]):
    """
    Render a summary card for a report.
    """
    tech = report.get("technical_analysis", {})
    news = report.get("news_analysis", {})
    pred = report.get("prediction", {})

    score = tech.get("score", 50)
    up_prob = pred.get("up_probability", 50)

    with st.container():
        st.markdown(f'<div class="report-card">', unsafe_allow_html=True)

        cols = st.columns([1, 2, 1])

        with cols[0]:
            st.markdown(f"### {stock_code}")
            change = tech.get("change_pct", 0)
            color = "#ef4444" if change >= 0 else "#10b981"
            st.markdown(
                f"<span style='color:{color}; font-size: 1.2em; font-weight:bold;'>{change}%</span>",
                unsafe_allow_html=True,
            )
            render_score_bar(score)

        with cols[1]:
            st.markdown("**🤖 AI 核心观点**")
            summary = news.get("summary", "暂无详细分析")
            st.info(summary)

            signals = tech.get("signals", [])
            if signals:
                st.markdown(
                    f"<span style='color:#94a3b8; font-size:0.9em;'>技术信号: {' '.join(signals[:3])}</span>",
                    unsafe_allow_html=True,
                )

        with cols[2]:
            render_probability_gauge(up_prob)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button(f"查看 {stock_code} 完整报告", key=f"btn_full_{stock_code}"):
            st.session_state["view_report_code"] = stock_code
            st.rerun()


def render_full_report(stock_code: str, report: Dict[str, Any]):
    """
    Render the full detail report.
    """
    if st.button("← 返回列表"):
        del st.session_state["view_report_code"]
        st.rerun()

    st.markdown(f"## 📑 {stock_code} 深度分析报告")
    st.caption(f"生成时间: {report.get('generated_at')}")

    tech = report.get("technical_analysis", {})
    news = report.get("news_analysis", {})
    pred = report.get("prediction", {})

    # 1. Prediction Section
    st.markdown("### 🔮 明日走势预测")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("综合评分", f"{tech.get('score', 0)}/100")
    with col2:
        up = pred.get("up_probability", 50)
        st.metric("上涨概率", f"{up}%", delta=f"{up - 50}%" if up != 50 else None)
    with col3:
        st.metric("主要信号", len(tech.get("signals", [])))

    # 2. Technical Analysis
    st.markdown("---")
    st.markdown("### 📈 技术面分析")
    signals = tech.get("signals", [])
    if signals:
        st.success(f"触发信号: {', '.join(signals)}")
    else:
        st.info("当前无明显技术形态信号")

    # 3. News Analysis
    st.markdown("---")
    st.markdown("### 📰 消息面解读")
    st.write(news.get("summary", "无"))

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🚀 利好因素**")
        catalysts = news.get("key_catalysts", [])
        if catalysts:
            for item in catalysts:
                st.markdown(f"- {item}")
        else:
            st.caption("暂无明显利好")

    with c2:
        st.markdown("**⚠️ 风险提示**")
        risks = news.get("risk_warnings", [])
        if risks:
            for item in risks:
                st.markdown(f"- {item}")
        else:
            st.caption("暂无明显风险")


def render_daily_reports():
    """
    Main entry point for the Daily Reports page.
    """
    st.title("📋 每日智能分析报告")

    today = datetime.date.today().strftime("%Y%m%d")
    watchlist = st.session_state.get("watchlist", [])

    if st.button("🔄 立即生成/刷新报告"):
        with st.spinner("正在生成最新报告..."):
            generate_all_reports(watchlist)
        st.rerun()

    # Check if viewing specific report
    if "view_report_code" in st.session_state:
        code = st.session_state["view_report_code"]
        report = load_report(today, code)
        if report:
            render_full_report(code, report)
        else:
            st.error(f"未找到 {code} 的报告")
            if st.button("返回"):
                del st.session_state["view_report_code"]
                st.rerun()
        return

    # List view
    st.markdown(f"**📅 日期: {today}** | 监控股票: {len(watchlist)} 只")

    reports_found = 0
    for code in watchlist:
        report = load_report(today, code)
        if report:
            render_report_card(code, report)
            reports_found += 1

    if reports_found == 0:
        st.warning("今日报告尚未生成。请点击上方按钮生成报告，或等待16:00后自动生成。")
