#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <unistd.h>

#include <job.h>
#include <logging.h>


void *user_thread(void *args)
{
    long long self = pthread_self();

    logging_info("user %lld logged in", self);

    char desc[] = "Job xxx from User xxxxxxxxxxxxx";
    for (int i = 0; i < 100; ++i)
    {
        int last = snprintf(desc, sizeof(desc)-1, "Job %03d from User %013lld", i+1, self);
        desc[last] = '\0';

        long long job_id = submit_job(self, desc);
        logging_info("user %lld submitted job %lld", self, job_id);

        sleep(random() % 10 + 2);
    }
    logging_info("user %lld logged out", self);

    return NULL;
}


int main(int argc, char *argv[])
{
    srand(time(NULL));

    job_system_init();


    for (int i = 0; i < 3; ++i)
    {
        pthread_t thread;
        pthread_create(&thread, NULL, user_thread, NULL);
        pthread_detach(thread);
    }

    while (1)
    {
        sleep(3);
    }

    return 0;
}
