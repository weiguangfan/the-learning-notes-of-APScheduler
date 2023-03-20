from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor
import logging

# increase the logging level of the apscheduler logger to the DEBUG level
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


EVENT_JOB_EXECUTED = ''
ECENT_JOB_ERROR = ''


jobstores = {
    'mongo':MongoDBJobStore(),
    'default':SQLAlchemyJobStore(url='sqlite:///jobs.sqlite'),
}

executors = {
    'default':ThreadPoolExecutor(20),
    'processpool':ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce':False,
    # limiting the number of concurrently executing instances  of a job
    'max_instances':3
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc
)


def my_listener(event):
    if event.exception:
        print('the job crashed:')
    else:
        print('the job worked:')


# pausing jobs
scheduler.pause_job()
# resuming jobs
scheduler.resume_job()
# getting a list of scheduled jobs
scheduler.get_jobs()
# a formatted list of jobs,their triggers and next run times
scheduler.print_jobs()
# modifying jobs
scheduler.modify_job()
# reschedule the job,that is,change its trigger
scheduler.reschedule_job('my_job_id',trigger='cron',minute='*/5')
# shutting down the scheduler
scheduler.shutdown()
# not until all currently executing jobs are finished.
scheduler.shutdown(wait=False)
# pausing/resuming job processing
scheduler.pause()
# wake up
scheduler.resume()
# without the first wakeup call,start the scheduler in paused state
scheduler.start(paused=True)
# scheduler events
# attach event listeners to the scheduler
# the event moudle for specifics on the available events and their attributes.
scheduler.add_listener(my_listener,EVENT_JOB_EXECUTED | ECENT_JOB_ERROR)




def myfunc():
    pass

# adding jobs
job = scheduler.add_job(myfunc,'interval',minutes=2)
# removing jobs
job.remove()
# pausing jobs
job.pause()
# resuming jobs
job.resume()
# modifying jobs
job.modify(max_isntances=6,name='Alternate name')
# reschedule the job,that is,change its trigger
job.reschedule()