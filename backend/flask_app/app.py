import os
from flask import Flask, send_from_directory
from . import config
from .routes import api

app = Flask(__name__, static_folder=None)
app.secret_key = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
app.register_blueprint(api)

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    dist = config.FRONTEND_FOLDER
    if path and os.path.exists(os.path.join(dist, path)):
        return send_from_directory(dist, path)
    index = os.path.join(dist, "index.html")
    if os.path.exists(index):
        return send_from_directory(dist, "index.html")
    return {"error": "Frontend not built. Run: cd frontend && npm install && npm run build"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
