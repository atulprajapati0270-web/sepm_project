import csv
import io
import os
from datetime import datetime
from urllib.request import Request, urlopen

from ..extensions import db
from ..models import Notification


def sync_google_updates():
    """Import rows from a public Google Sheets CSV, when configured."""
    sheet_url = os.getenv("GOOGLE_SHEET_CSV_URL", "").strip()
    if not sheet_url:
        return 0

    try:
        request = Request(sheet_url, headers={"User-Agent": "SimhasthaUpdates/1.0"})
        with urlopen(request, timeout=5) as response:
            content = response.read().decode("utf-8-sig")
        rows = csv.DictReader(io.StringIO(content))
        imported = 0
        for row in rows:
            title = (row.get("title") or row.get("Title") or "").strip()
            message = (row.get("message") or row.get("Message") or "").strip()
            priority = (row.get("priority") or row.get("Priority") or "Normal").strip() or "Normal"
            if not title or not message:
                continue
            existing = Notification.query.filter_by(title=title, message=message).first()
            if existing:
                existing.priority = priority
                continue
            db.session.add(Notification(title=title, message=message, priority=priority, date=datetime.utcnow()))
            imported += 1
        if imported or rows:
            db.session.commit()
        return imported
    except Exception:
        db.session.rollback()
        return 0
