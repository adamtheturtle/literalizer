#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        unsigned long long u;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
static void api_worker_process_stub_(CVal _a0, CVal _a1) { (void)_a0, (void)_a1; }
struct workerType_ { void (*process)(CVal, CVal); };
struct apiType_ { struct workerType_ worker; };
static const struct apiType_ api = { .worker = { .process = api_worker_process_stub_ } };
int main(void) {
api.worker.process(((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.m = (CKV[]){}})}}), ((CVal){.i = 42}));
api.worker.process(((CVal){.a = (CVal[]){((CVal){.i = 2}), ((CVal){.m = (CKV[]){{"x", ((CVal){.s = "s"})}}})}}), ((CVal){.i = 43}));
    return 0;
}
