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
static void api_process_stub_(CVal _a0) { (void)_a0; }
struct apiType_ { void (*process)(CVal); };
static const struct apiType_ api = { .process = api_process_stub_ };
int main(void) {
api.process(((CVal){.m = (CKV[]){}}));
    return 0;
}
