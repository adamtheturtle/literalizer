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
static void app_mgr_run_stub_(CVal _a0) { (void)_a0; }
struct mgrType_ { void (*run)(CVal); };
struct appType_ { struct mgrType_ mgr; };
static const struct appType_ app = { .mgr = { .run = app_mgr_run_stub_ } };
int main(void) {
app.mgr.run(((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_1"})}, {"draft", ((CVal){.b = true})}}}));
app.mgr.run(((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_2"})}}}));
    return 0;
}
