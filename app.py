from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')  # Serve the saved HTML file

if __name__ == "__main__":
    app.run(debug=True)

