import json
from flask import Flask, request, Response
from process import classify

app = Flask(__name__)


# Define a simple route
@app.route('/api/classify', methods=['GET', 'POST'])
def index():
    docs = request.args.get('docs')
    return Response(json.dumps(classify(docs), ensure_ascii=False).encode('utf-8'),
                    content_type='text/html; charset=utf-8')


if __name__ == '__main__':
    app.run(port=8000)
