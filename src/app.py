import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from calculator import calculate_expression
from database import (
    init_db, save_history, get_all_history,
    delete_history, clear_all_history
)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    if not data or 'expression' not in data:
        return jsonify({
            "success": False,
            "message": "缺少 expression 字段"
        }), 400

    expression = data['expression'].strip()
    if not expression:
        return jsonify({
            "success": False,
            "message": "表达式不能为空"
        }), 400

    try:
        result = calculate_expression(expression)
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    except Exception:
        return jsonify({
            "success": False,
            "message": "服务器内部错误"
        }), 500

    save_history(expression, result)

    return jsonify({
        "success": True,
        "expression": expression,
        "result": result
    })


@app.route('/api/history', methods=['GET'])
def history():
    records = get_all_history()
    return jsonify({
        "success": True,
        "history": records
    })


@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if delete_history(record_id):
        return jsonify({
            "success": True,
            "message": "删除成功"
        })
    return jsonify({
        "success": False,
        "message": "记录不存在"
    }), 404


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    count = clear_all_history()
    return jsonify({
        "success": True,
        "message": f"已清空 {count} 条记录"
    })


init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)