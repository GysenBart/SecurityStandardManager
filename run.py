from app import app
from app.util import run_cloning_repo
from config import debug_enabled, host, port
import threading

if __name__ == "__main__":
    thread = threading.Thread(target=run_cloning_repo)
    thread.start()
    app.run(debug=debug_enabled, host=host, port=port)