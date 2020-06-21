import helper
from flask import Flask, request, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)

@app.route('/member/new', methods=['POST'])
def add_member():
    req_data = request.get_json()

    # Add member to database
    res_data = helper.add_member(req_data)

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

    group = request.args.get('group')
    res_data = helper.get_all_member(group)

    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/member', methods=['GET'])
def get_member():
    
    name = request.args.get('name')
    group = request.args.get('group')

    # Get items from the helper
    status = helper.get_member(name, group)

    # Return 404 if item not found
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    res_data = {
        'member': status
    }

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/member/update', methods=['PUT'])
def update_member():

    req_data = request.get_json()

    res_data = helper.update_member(req_data)

    # Return error if the status could not be updated
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
def delete_member():
    req_data = request.get_json()

    # Delete item from the list
    res_data = helper.delete_member(req_data)

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
def add_column():
    req_data = request.get_json()

    # Add item to the list
    res_data = helper.add_column(req_data)

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
def delete_column():
    req_data = request.get_json()

    res_data = helper.delete_column(req_data)

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
    
    group = request.args.get('group')

    # Get items from the helper
    columns = helper.get_table(group)

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
    