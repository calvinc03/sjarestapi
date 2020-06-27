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

    validated = validateRequest(request)
    if validated != "validated":
        return validated

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

    validated = validateGETRequest(request)
    if validated != "validated":
        return validated

    res_data = helper.get_all_member()

    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/member/names', methods=['GET'])
def get_member_names():

    validated = validateGETRequest(request)
    if validated != "validated":
        return validated

    res_data = helper.get_member_names()

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
    
    validated = validateRequest(request)
    if validated != "validated":
        return validated

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
    
    validated = validateRequest(request)
    if validated != "validated":
        return validated

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
    
    validated = validateRequest(request)
    if validated != "validated":
        return validated

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
    
    validated = validateRequest(request)
    if validated != "validated":
        return validated

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

    validated = validateGETRequest(request)
    if validated != "validated":
        return validated
        
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
    
    validated = validateRequest(request)
    if validated != "validated":
        return validated

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

@app.route("/login", methods=["POST"])
def login():
    req_data = request.get_json()

    # Get items from the helper
    res_data = helper.login(req_data)

    # Return 404 if item not found
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/auth", methods=["POST"])
def auth():
    req_data = request.get_json()

    token = req_data['access_token']
    # Get items from the helper
    res_data = helper.auth(token)

    # Return 400 if item not found
    if 'error' in res_data:
        response = Response(json.dumps(res_data), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # Return response
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def validateRequest(request):
    if 'token' not in request.headers or 'Content-Type' not in request.headers:
        response = Response(json.dumps({'error': 'Incomplete Headers'}), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    access_token = request.headers['token']
    auth = helper.auth(access_token)

    if 'error' in auth:
        response = Response(json.dumps(auth), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    if auth['permissions'] != 'Admin':
        response = Response(json.dumps({'error': 'This user does not have permission to perform this action'}), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    return "validated"


def validateGETRequest(request):
    if 'token' not in request.headers:
        response = Response(json.dumps({'error': 'Incomplete Headers'}), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    access_token = request.headers['token']
    auth = helper.auth(access_token)

    if 'error' in auth:
        response = Response(json.dumps(auth), status=400, mimetype='application/json')
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    return "validated"