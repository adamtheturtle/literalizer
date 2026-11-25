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
static void process_api_fetch_stub_(CVal _a0) { (void)_a0; }
struct apiType_ { void (*fetch)(CVal); };
struct processType_ { struct apiType_ api; };
static const struct processType_ process = { .api = { .fetch = process_api_fetch_stub_ } };
int main(void) {
process.api.fetch(((CVal){.m = (CKV[]){{"data", ((CVal){.s = "hello"})}}}));
process.api.fetch(((CVal){.m = (CKV[]){{"data", ((CVal){.i = 42})}}}));
process.api.fetch(((CVal){.m = (CKV[]){{"data", ((CVal){.b = true})}}}));
    return 0;
}
