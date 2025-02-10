from app import app, scheduler
from config import debug_enabled, host, port

if __name__ == "__main__":
    scheduler.start()
    app.run(debug=debug_enabled, host=host, port=port)