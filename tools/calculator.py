import ast
import operator

from langchain.tools import tool

#定义允许哪些数学运算
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


@tool("calculator")     #定义工具 工具名"calculator"
def calculator(expression: str) -> str:         #expression表示问题 在这里是128*36
    """计算简单数学表达式，例如 128 * 36。"""
    result = _safe_eval(expression)
    return str(result)

#安全地解析数学表达式
def _safe_eval(expression: str) -> int | float:
    tree = ast.parse(expression, mode="eval")       #把字符串解析成语法树 然后我们手动判断哪些节点允许执行
    return _eval_node(tree.body)

#递归计算语法树里的节点。
def _eval_node(node) -> int | float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("不支持的运算符")

        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("不支持的运算符")

        operand = _eval_node(node.operand)
        return _ALLOWED_OPERATORS[operator_type](operand)

    raise ValueError("只支持简单数学表达式")