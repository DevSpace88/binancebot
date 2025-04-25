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
        """Starts the scheduler"""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return

        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        self.logger.info("Scheduler started")

    def stop(self):
        """Stops the scheduler"""
        if not self.running:
            self.logger.warning("Scheduler is not running")
            return

        self.running = False
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5.0)

        self.logger.info("Scheduler stopped")

    def _run_scheduler(self):
        """Thread function for the scheduler"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def add_job(self, job_id: str, interval: str, job_func: Callable, *args, **kwargs):
        """
        Adds a job to the scheduler

        Args:
            job_id: Unique ID for the job
            interval: Interval as a string ('1h', '30m', '1d', etc.)
            job_func: Function to be executed
            *args, **kwargs: Arguments for the function
        """
        if job_id in self.jobs:
            self.logger.warning(f"Job with ID {job_id} already exists. Will be overwritten.")
            self.remove_job(job_id)

        # Parse interval
        if interval.endswith('m'):
            # Minutes
            minutes = int(interval[:-1])
            job = schedule.every(minutes).minutes.do(job_func, *args, **kwargs)
        elif interval.endswith('h'):
            # Hours
            hours = int(interval[:-1])
            job = schedule.every(hours).hours.do(job_func, *args, **kwargs)
        elif interval.endswith('d'):
            # Days
            days = int(interval[:-1])
            job = schedule.every(days).days.do(job_func, *args, **kwargs)
        else:
            # Default interpret as hours
            hours = int(interval)
            job = schedule.every(hours).hours.do(job_func, *args, **kwargs)

        self.jobs[job_id] = job
        self.logger.info(f"Job {job_id} with interval {interval} added")

    def remove_job(self, job_id: str) -> bool:
        """
        Removes a job from the scheduler

        Args:
            job_id: ID of the job to be removed

        Returns:
            True if the job was removed, otherwise False
        """
        if job_id in self.jobs:
            schedule.cancel_job(self.jobs[job_id])
            del self.jobs[job_id]
            self.logger.info(f"Job {job_id} removed")
            return True
        else:
            self.logger.warning(f"Job {job_id} does not exist")
            return False

    def get_jobs(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all active jobs

        Returns:
            List with job information
        """
        job_list = []
        for job_id, job in self.jobs.items():
            next_run = job.next_run
            if next_run:
                next_run_str = next_run.strftime('%Y-%m-%d %H:%M:%S')
            else:
                next_run_str = 'Not scheduled'

            job_list.append({
                'id': job_id,
                'next_run': next_run_str,
                'interval': str(job.interval),
                'unit': job.unit
            })

        return job_list