# main.py
import os
import sys
from datetime import datetime
from importlib.metadata import version

from dotenv import load_dotenv
from flask import Flask, jsonify

from .models import RequestLog, get_db_session

# Load .env file, but allow environment variables to override
load_dotenv(override=False)
app = Flask(__name__)


@app.route("/")
def hello():
    """Return app status and store request in database."""
    # Get current request metadata
    current_data = {
        "debug_mode": str(app.debug),
        "flask_version": version("flask"),
        "python_version": sys.version,
        "environment": os.environ["FLASK_ENV"],
        "service_name": os.environ["SERVICE_NAME"],
        "port": os.environ["PORT"],
        "timestamp": datetime.now().isoformat(),
    }

    try:
        # Get database session - will fail if DB is not available
        database_url = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
        session = get_db_session(database_url=database_url)

        # Store current request in database
        request_log = RequestLog(
            timestamp=datetime.now(),
            environment=current_data["environment"],
            flask_version=current_data["flask_version"],
            python_version=current_data["python_version"],
            debug_mode=current_data["debug_mode"],
            port=current_data["port"],
            service_name=current_data["service_name"],
        )
        session.add(request_log)
        session.commit()

        # Retrieve last 5 requests from database
        recent_requests = (
            session.query(RequestLog)
            .order_by(RequestLog.timestamp.desc())
            .limit(10)
            .all()
        )

        # Close session
        session.close()

        # Add database status and history to response
        current_data["recent_requests"] = [req.to_dict() for req in recent_requests]

    except Exception as e:
        # If database connection fails, the entire endpoint fails
        # This demonstrates the hard dependency on the database
        return (
            jsonify({"details": str(e)}),
            503,
        )

    return jsonify(current_data)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/echo/<text>")
def echo(text):
    return jsonify({"you_said": text, "reversed": text[::-1], "length": len(text)})
