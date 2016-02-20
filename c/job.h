#ifndef JOB_H
#define JOB_H            1

#include <time.h>

#include <pthread.h>

#include <list.h>


#define JOB_EVENT_SUBMITTED        0
#define JOB_EVENT_COMPLETED        1
#define JOB_EVENT_SCHED            2

#define JOB_STATUS_CREATED         0
#define JOB_STATUS_RUNNABLE        1
#define JOB_STATUS_RUNNING         2
#define JOB_STATUS_ABORTED         4
#define JOB_STATUS_RETIRED         8

#define JOB_USER_NONE              -1
#define JOB_DESC_MAX               128

typedef struct job
{
    long long id;
    int status;

    long long user_id;
    char desc[JOB_DESC_MAX];

    time_t submitted;
    time_t started;
    time_t ended;

    pthread_mutex_t mutex;

    list_head_t link;
    list_head_t queue;
} job_t;


#define job_entry(ref) list_entry(job_t, link, ref)
#define job_entry_on_queue(ref) list_entry(job_t,queue,ref)

typedef struct job_queue
{
    list_t jobs;
    pthread_mutex_t mutex;
} job_queue_t;


extern int job_init(job_t *job, long long id, int status);
extern job_t *job_new(void);

extern int job_queue_init(job_queue_t *queue);
extern job_queue_t *job_queue_new(void);

extern void dumps_job(const job_t *job);
extern void dumps_job_queue(const job_queue_t *queue);

extern int job_system_init(void);

extern long long submit_job(long long user_id, const char *description);
extern long long cancel_job(long long id);


#endif
