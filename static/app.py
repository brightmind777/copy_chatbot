from flask import Flask, send_from_directory, render_template
from serverless_http import handle_request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/audio/<filename>')
def audio(filename):
    directory = os.path.join(app.root_path, 'static', 'audio')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True)

handler = handle_request(app)