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
static void app_process_fetch_stub_(CVal _a0) { (void)_a0; }
struct processType_ { void (*fetch)(CVal); };
struct appType_ { struct processType_ process; };
static const struct appType_ app = { .process = { .fetch = app_process_fetch_stub_ } };
int main(void) {
app.process.fetch(((CVal){.m = (CKV[]){{"data", ((CVal){.s = "hello"})}}}));
app.process.fetch(((CVal){.m = (CKV[]){{"data", ((CVal){.i = 42})}}}));
app.process.fetch(((CVal){.m = (CKV[]){{"data", ((CVal){.b = true})}}}));
    return 0;
}
