import ast, operator
from datetime import datetime, timezone
from typing import Annotated
import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from tavily import TavilyClient
from app.core.config import get_settings

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
       ast.UAdd: operator.pos, ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv}

def safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        a, b = safe_eval(node.left), safe_eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(b) > 8: raise ValueError("Exponent too large")
        return OPS[type(node.op)](a, b)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.operand))
    raise ValueError("Only basic arithmetic is allowed")

@tool
def calculator(expression: Annotated[str, "Arithmetic expression, e.g. (125 * 4) / 5"]) -> str:
    "Calculate arithmetic using a restricted expression evaluator."
    try: return str(safe_eval(ast.parse(expression, mode="eval").body))
    except Exception as exc: return f"Calculation error: {exc}"

@tool
def current_utc_time() -> str:
    "Return the current UTC date and time."
    return datetime.now(timezone.utc).isoformat()

@tool
def web_search(query: Annotated[str, "Focused web search query"]) -> str:
    "Search the web for current information. Requires TAVILY_API_KEY."
    key = get_settings().tavily_api_key
    if not key: return "Web search is not configured. Add TAVILY_API_KEY to .env."
    try:
        result = TavilyClient(api_key=key).search(query=query, max_results=5, search_depth="advanced")
        return str(result.get("results", []))
    except Exception as exc: return f"Search failed: {exc}"

@tool
def fetch_webpage(url: Annotated[str, "Public http or https URL"]) -> str:
    "Extract readable text from a public webpage."
    if not url.startswith(("http://", "https://")): return "Only http/https URLs are allowed."
    try:
        with httpx.Client(timeout=15, follow_redirects=True, headers={"User-Agent":"AtlasAgent/1.0"}) as client:
            response = client.get(url); response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script","style","nav","footer","header","noscript"]): tag.decompose()
        return " ".join(soup.get_text(" ").split())[:12000] or "No readable text found."
    except Exception as exc: return f"Page fetch failed: {exc}"

TOOLS = [calculator, current_utc_time, web_search, fetch_webpage]
