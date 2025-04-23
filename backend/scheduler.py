# scheduler.py
import time
import threading
import schedule
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable


class Scheduler:
    def __init__(self):
        self.logger = logging.getLogger('Scheduler')
        self.running = False
        self.scheduler_thread = None
        self.jobs = {}

    def start(self):
        """Startet den Scheduler"""
        if self.running:
            self.logger.warning("Scheduler läuft bereits")
            return

        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        self.logger.info("Scheduler gestartet")

    def stop(self):
        """Stoppt den Scheduler"""
        if not self.running:
            self.logger.warning("Scheduler läuft nicht")
            return

        self.running = False
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5.0)

        self.logger.info("Scheduler gestoppt")

    def _run_scheduler(self):
        """Thread-Funktion für den Scheduler"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def add_job(self, job_id: str, interval: str, job_func: Callable, *args, **kwargs):
        """
        Fügt einen Job zum Scheduler hinzu

        Args:
            job_id: Eindeutige ID für den Job
            interval: Intervall als String ('1h', '30m', '1d', usw.)
            job_func: Funktion, die ausgeführt werden soll
            *args, **kwargs: Argumente für die Funktion
        """
        if job_id in self.jobs:
            self.logger.warning(f"Job mit ID {job_id} existiert bereits. Wird überschrieben.")
            self.remove_job(job_id)

        # Intervall parsen
        if interval.endswith('m'):
            # Minuten
            minutes = int(interval[:-1])
            job = schedule.every(minutes).minutes.do(job_func, *args, **kwargs)
        elif interval.endswith('h'):
            # Stunden
            hours = int(interval[:-1])
            job = schedule.every(hours).hours.do(job_func, *args, **kwargs)
        elif interval.endswith('d'):
            # Tage
            days = int(interval[:-1])
            job = schedule.every(days).days.do(job_func, *args, **kwargs)
        else:
            # Standardmäßig als Stunden interpretieren
            hours = int(interval)
            job = schedule.every(hours).hours.do(job_func, *args, **kwargs)

        self.jobs[job_id] = job
        self.logger.info(f"Job {job_id} mit Intervall {interval} hinzugefügt")

    def remove_job(self, job_id: str) -> bool:
        """
        Entfernt einen Job aus dem Scheduler

        Args:
            job_id: ID des zu entfernenden Jobs

        Returns:
            True, wenn der Job entfernt wurde, sonst False
        """
        if job_id in self.jobs:
            schedule.cancel_job(self.jobs[job_id])
            del self.jobs[job_id]
            self.logger.info(f"Job {job_id} entfernt")
            return True
        else:
            self.logger.warning(f"Job {job_id} existiert nicht")
            return False

    def get_jobs(self) -> List[Dict[str, Any]]:
        """
        Gibt eine Liste aller aktiven Jobs zurück

        Returns:
            Liste mit Job-Informationen
        """
        job_list = []
        for job_id, job in self.jobs.items():
            next_run = job.next_run
            if next_run:
                next_run_str = next_run.strftime('%Y-%m-%d %H:%M:%S')
            else:
                next_run_str = 'Nicht geplant'

            job_list.append({
                'id': job_id,
                'next_run': next_run_str,
                'interval': str(job.interval),
                'unit': job.unit
            })

        return job_list


