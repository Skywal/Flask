from app import app
from config import is_debug

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=is_debug)
