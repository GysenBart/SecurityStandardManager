from app import app, scheduler
from app.util import run_cloning_repo
from config import debug_enabled, host, port

if __name__ == "__main__":
    scheduler.start()
    app.run(debug=debug_enabled, host=host, port=port)