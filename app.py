from __future__ import annotations

from flask import Flask, jsonify, request, send_from_directory

from fbref_scraper import FBRefScrapeError, scrape_season_schedule

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index() -> str:
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/scrape")
def scrape():
    payload = request.get_json(force=True, silent=True) or {}
    season = (payload.get("season") or "").strip()
    try:
        fixtures = scrape_season_schedule(season)
        return jsonify({"season": season, "fixtures": fixtures})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except FBRefScrapeError as exc:  # pragma: no cover - network
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:  # pragma: no cover - defensive
        return jsonify({"error": f"Unexpected error: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
