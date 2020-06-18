import helper
from flask import Flask, request, Response
import json

app = Flask(__name__)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)

@app.route('/member/new', methods=['POST'])
def add_member():
    req_data = request.get_json()

    # Add item to the list
    res_data = helper.add_member(req_data)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Member not added - " + req_data['name'] + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/member/all')
def get_all_member():

    group = request.args.get('group')
    res_data = helper.get_all_member(group)

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/member', methods=['GET'])
def get_member():
    
    name = request.args.get('name')
    group = request.args.get('group')

    # Get items from the helper
    status = helper.get_member(name, group)

    # Return 404 if item not found
    if status is None:
        response = Response("{'error': 'Member Not Found - %s'}"  % name, status=404 , mimetype='application/json')
        return response

    # Return status
    res_data = {
        'name': name
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/member/update', methods=['PUT'])
def update_member():

    req_data = request.get_json()

    res_data = helper.update_member(req_data)

    # Return error if the status could not be updated
    if res_data is None:
        response = Response("{'error': 'Error updating member - '" + req_data['name'] + "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/member/remove', methods=['DELETE'])
def delete_member():
    req_data = request.get_json()

    # Delete item from the list
    res_data = helper.delete_member(req_data)

    # Return error if the item could not be deleted
    if res_data is None:
        response = Response("{'error': 'Error deleting member - '" + req_data['name'] +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/column/new', methods=['POST'])
def add_column():
    req_data = request.get_json()

    # Add item to the list
    res_data = helper.add_column(req_data)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Column not added - " + req_data['column'] + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/column/remove', methods=['DELETE'])
def delete_column():
    req_data = request.get_json()

    res_data = helper.delete_column(req_data)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Error deleting column - " + req_data['column'] + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/table', methods=['GET'])
def get_table():
    
    group = request.args.get('group')

    # Get items from the helper
    columns = helper.get_table(group)

    # Return 404 if item not found
    if columns is None:
        response = Response("{'error': 'Table Not Found - %s'}"  % group, status=404 , mimetype='application/json')
        return response

    # Return status
    res_data = {
        'table': columns
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response