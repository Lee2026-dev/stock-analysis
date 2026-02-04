from src.logic.report_engine import generate_report_for_stock, generate_all_reports
from src.utils.scheduler import should_generate_report, is_trading_day
import datetime
import json


def test_report_generation():
    print("Testing Report Generation...")
    code = "000001"
    date = datetime.date.today().strftime("%Y%m%d")

    try:
        report = generate_report_for_stock(code, date)
        print(f"Report Generated for {code}")

        print(f"Tech Score: {report['technical_analysis']['score']}")
        print(f"Sentiment Score: {report['news_analysis']['sentiment_score']}")
        print(f"Prediction: {report['prediction']['up_probability']}% Up")

        print("Report structure valid.")
    except Exception as e:
        print(f"Report generation failed: {e}")


def test_scheduler():
    print("\nTesting Scheduler...")
    is_trading = is_trading_day()
    print(f"Is today trading day? {is_trading}")

    should = should_generate_report()
    print(f"Should generate? {should}")


if __name__ == "__main__":
    test_scheduler()
    test_report_generation()
