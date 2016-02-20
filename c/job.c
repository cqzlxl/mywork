#include <assert.h>
#include <stdlib.h>
#include <time.h>

#include <pthread.h>
#include <unistd.h>

#include <event.h>
#include <job.h>
#include <list.h>
#include <logging.h>


static long long next_job_id = 1;
static pthread_mutex_t next_job_id_mutex = PTHREAD_MUTEX_INITIALIZER;


static long long accuire_next_job_id()
{
    pthread_mutex_lock(&next_job_id_mutex);
    long long id = next_job_id++;
    pthread_mutex_unlock(&next_job_id_mutex);
    return id;
}


static event_bus_t *event_bus;
static job_queue_t *jobs_all;
static job_queue_t *jobs_created;
static job_queue_t *jobs_running;
static job_queue_t *jobs_aborted;
static job_queue_t *jobs_retired;
static job_queue_t *jobs_canceled;

static pthread_t scheduler;


static void *scheduler_thread(void *args)
{
    long long self = pthread_self();
    logging_debug("scheduler %lld starts", self);

    while (1)
    {
        event_bus_wait(event_bus, JOB_EVENT_SUBMITTED);

        pthread_mutex_lock(&jobs_created->mutex);
        job_t *job = NULL;
        list_for_each(&jobs_created->jobs, link)
        {
            job_t *j = job_entry_on_queue(link);
            if (j->status == JOB_STATUS_CREATED)
            {
                job = j;
                break;
            }
        }
        if (job == NULL)
        {
            logging_warn("waked up by submit event, but no new job found");
        }
        else
        {
            list_delete(&jobs_created->jobs, &job->queue);
        }
        pthread_mutex_unlock(&jobs_created->mutex);

        if (job == NULL)
        {
            continue;
        }

        job->status = JOB_STATUS_RUNNABLE;
        job->started = time(NULL);

        pthread_mutex_lock(&jobs_running->mutex);
        list_prepend(&jobs_running->jobs, &job->queue);
        pthread_mutex_unlock(&jobs_running->mutex);

        event_bus_signal(event_bus, JOB_EVENT_SCHED);
        logging_info("scheduled Job %lld to run", job->id);
    }

    logging_debug("scheduler %lld done", self);

    return NULL;
}


static void *executor_thread(void *args)
{
    long long self = pthread_self();
    logging_debug("executor %lld starts", self);

    while (1)
    {
        event_bus_wait(event_bus, JOB_EVENT_SCHED);

        pthread_mutex_lock(&jobs_running->mutex);
        job_t *job = NULL;
        list_for_each(&jobs_running->jobs, link)
        {
            job_t *j = job_entry_on_queue(link);
            if (j->status == JOB_STATUS_RUNNABLE)
            {
                job = j;
                break;
            }
        }
        if (job == NULL)
        {
            logging_warn("waked up by sched event, but no runnable job found");
        }
        else
        {
            job->status = JOB_STATUS_RUNNING;
        }
        pthread_mutex_unlock(&jobs_running->mutex);

        if (job == NULL)
        {
            continue;
        }

        dumps_job(job);
        int interval = random() % 20 + 2;
        sleep(interval);

        event_bus_signal(event_bus, JOB_EVENT_COMPLETED);
        logging_info("executor %lld done job %lld in %d seconds", self, job->id, interval);
    }

    logging_debug("executor %lld done", self);

    return NULL;
}


int job_init(job_t *job, long long id, int status)
{
    assert(job != NULL);

    job->id = id;
    job->status = status;

    job->user_id = JOB_USER_NONE;
    job->desc[0] = '\0';

    job->submitted = time(NULL);
    job->started = -1;
    job->ended = -1;

    pthread_mutex_init(&job->mutex, NULL);

    list_head_init(&job->link);
    list_head_init(&job->queue);

    return 0;
}


job_t *job_new(void)
{
    job_t *job = malloc(sizeof(job_t));
    assert(job != NULL);

    job_init(job, accuire_next_job_id(), JOB_STATUS_CREATED);

    return job;
}


int job_queue_init(job_queue_t *queue)
{
    assert(queue != NULL);

    list_init(&queue->jobs);
    pthread_mutex_init(&queue->mutex, NULL);

    return 0;
}


job_queue_t *job_queue_new(void)
{
    job_queue_t *q = malloc(sizeof(job_queue_t));
    assert(q != NULL);

    job_queue_init(q);

    return q;
}


void dumps_job(const job_t *job)
{
    logging_debug("Job %lld: status=%d, user_id=%lld, desc=%s", job->id, job->status, job->user_id, job->desc);
}


int job_system_init(void)
{
    event_bus = event_bus_new();
    jobs_all = job_queue_new();
    jobs_created = job_queue_new();
    jobs_running = job_queue_new();
    jobs_aborted = job_queue_new();
    jobs_retired = job_queue_new();
    jobs_canceled = job_queue_new();

    pthread_create(&scheduler, NULL, scheduler_thread, NULL);
    pthread_detach(scheduler);

    for (int i = 0; i < 20; ++i)
    {
        pthread_t executor;
        pthread_create(&executor, NULL, executor_thread, NULL);
        pthread_detach(executor);
    }

    return 0;
}


long long submit_job(long long user_id, const char *description)
{
    job_t *job = job_new();
    job->user_id = user_id;
    int last = snprintf(job->desc, JOB_DESC_MAX-1, "%s", description);
    job->desc[last] = '\0';

    list_prepend(&jobs_all->jobs, &job->link);
    logging_debug("job created: %lld", job->id);
    dumps_job(job);

    list_prepend(&jobs_created->jobs, &job->queue);
    event_bus_signal(event_bus, JOB_EVENT_SUBMITTED);
    logging_debug("job submitted: %lld", job->id);

    return job->id;
}
