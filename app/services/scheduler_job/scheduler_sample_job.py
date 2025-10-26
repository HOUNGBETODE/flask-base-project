from core.scheduler.scheduler import scheduler

def sample_job():
    with scheduler.app.app_context():
        print("[+] Implemented job...")
