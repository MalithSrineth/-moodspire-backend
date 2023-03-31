from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/post-example', methods=['POST'])
def post_example():
    # Get the data from the request
    data = request.get_json()
    print(data)
    # Do something with the data
    result = data['message']
    # Return the result as JSON
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run()
