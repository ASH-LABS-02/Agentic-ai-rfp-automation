from apscheduler.schedulers.background import BackgroundScheduler
from agents.tender_fetch_agent import fetch_pdfs_from_site
from agents.status_store import add_status

scheduler = BackgroundScheduler()

def scheduled_job(site_url: str):
    files = fetch_pdfs_from_site(site_url)
    for f in files:
        add_status(f"📄 Auto-downloaded {f}")

def start_scheduler(minutes: int, site_url: str):
    scheduler.remove_all_jobs()
    scheduler.add_job(
        scheduled_job,
        "interval",
        minutes=minutes,
        args=[site_url]
    )
    scheduler.start()
