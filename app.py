import helper
from flask import Flask, request, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)

@app.route('/member/new', methods=['POST'])
def add_members():
    req_data = request.get_json()

    # Add member to database
    res_data = helper.add_members(req_data)

    # Return error if exception is raised
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/member/all', methods=['GET'])
def get_all_member():

    res_data = helper.get_all_member()

    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/group/update', methods=['POST'])
def update_group():

    req_data = request.get_json()

    res_data = helper.update_group(req_data)

    # Return error if the status could not be updated
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/member/remove', methods=['DELETE'])
def delete_members():
    req_data = request.get_json()

    # Delete item from the list
    res_data = helper.delete_members(req_data)

    # Return error if the item could not be deleted
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/column/new', methods=['POST'])
def add_columns():
    req_data = request.get_json()

    # Add item to the list
    res_data = helper.add_columns(req_data)

    # Return error if item not added
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/column/remove', methods=['DELETE'])
def delete_columns():
    req_data = request.get_json()

    res_data = helper.delete_columns(req_data)

    # Return error if item not added
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/table', methods=['GET'])
def get_table():

    # Get items from the helper
    columns = helper.get_table()

    # Return 404 if item not found
    if 'error' in columns:
        response = Response(json.dumps(columns), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    res_data = {
        'table': columns
    }

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/email', methods=['POST'])
def send_email():
    
    req_data = request.get_json()

    # Get items from the helper
    res_data = helper.send_email(req_data)

    # Return 404 if item not found
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response