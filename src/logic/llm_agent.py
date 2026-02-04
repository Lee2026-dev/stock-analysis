import os
import json
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logger
logger = logging.getLogger(__name__)


def analyze_news_sentiment(news_list: List[Dict], stock_name: str) -> Dict:
    """
    Analyze news sentiment using LLM.

    Args:
        news_list: List of news items (title, content)
        stock_name: Stock name

    Returns:
        Dict: JSON response with sentiment_score, etc.
    """
    if not news_list:
        return {
            "sentiment_score": 50,
            "summary": "无消息面数据",
            "key_catalysts": [],
            "risk_warnings": [],
        }

    api_key = os.getenv("OPENAI_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if not api_key:
        logger.warning("No LLM API key found")
        return {
            "sentiment_score": 50,
            "summary": "API Key缺失",
            "key_catalysts": [],
            "risk_warnings": [],
        }

    try:
        # Construct prompt
        news_text = json.dumps(news_list, ensure_ascii=False)
        prompt = f"""
        角色：资深A股分析师
        任务：分析以下新闻对{stock_name}的影响
        
        新闻数据：
        {news_text}
        
        请输出JSON格式：
        {{
          "sentiment_score": 0-100,  // 0=极度悲观, 100=极度乐观
          "key_catalysts": ["利好1", "利好2"],
          "risk_warnings": ["风险1"],
          "summary": "100字以内的总结"
        }}
        """

        # Call LLM
        import openai

        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial analyst. Output valid JSON only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty LLM response")

        result = json.loads(content)
        return result

    except Exception as e:
        logger.error(f"LLM analysis failed: {e}")
        return {
            "sentiment_score": 50,
            "summary": "AI分析服务暂时不可用",
            "key_catalysts": [],
            "risk_warnings": [],
        }
