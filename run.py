from app import app
from config import debug_enabled, host, port

if __name__ == "__main__":
    app.run(debug=debug_enabled, host=host, port=port)