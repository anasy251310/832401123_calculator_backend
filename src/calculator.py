from asteval import Interpreter


def normalize_expression(expression: str) -> str:
    replacements = {
        '（': '(', '）': ')',
        '＋': '+', '－': '-', '—': '-', '–': '-',
        '×': '*', '＊': '*', '·': '*',
        '÷': '/', '／': '/',
        '．': '.', '。': '.',
        '，': ',', '　': ' ',
        '［': '[', '］': ']',
        '｛': '{', '｝': '}',
        '＾': '**',
    }
    for cn, en in replacements.items():
        expression = expression.replace(cn, en)
    return expression


def calculate_expression(expression: str):
    if not expression or not expression.strip():
        raise ValueError("表达式不能为空")

    expr = normalize_expression(expression).strip()

    aeval = Interpreter()
    result = aeval(expr)

    if aeval.error:
        error_msg = aeval.error[0].get_error()[1]
        raise ValueError(f"表达式错误: {error_msg}")

    if result is None:
        raise ValueError("表达式无法计算")
    if isinstance(result, float) and result == float('inf'):
        raise ValueError("除数不能为 0")

    if isinstance(result, float) and result == int(result):
        return int(result)
    return result