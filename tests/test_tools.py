import ast
import pytest
from app.agent.tools import safe_eval

def test_safe_arithmetic():
    assert safe_eval(ast.parse("(125 * 4) / 5", mode="eval").body) == 100

@pytest.mark.parametrize("expression", ["__import__('os')", "().__class__", "open('/etc/passwd')"])
def test_reject_unsafe_expression(expression):
    with pytest.raises((ValueError, TypeError)):
        safe_eval(ast.parse(expression, mode="eval").body)
