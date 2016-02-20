#include <assert.h>
#include <stdlib.h>

#include <list.h>
#include <logging.h>


typedef struct job {
    int id;
    list_head_t link;
} job_t;

#define job_entry(ref) list_entry(job_t,link,ref)


list_t job_list;


int main(int argc, char *argv[])
{
    list_init(&job_list);

    for (int i = 0; i < 4; ++i)
    {
        job_t *j = malloc(sizeof(job_t));
        assert(j != NULL);

        j->id = i + 100;
        list_head_init(&j->link);

        list_prepend(&job_list, &j->link);
    }

    list_for_each(&job_list, link)
    {
        job_t *j = job_entry(link);

        logging_info("Job %d", j->id);
    }

    return 0;
}
