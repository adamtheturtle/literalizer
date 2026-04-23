#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
static void mgr_Op_stub_(CVal _a0) { (void)_a0; }
struct mgrType_ { void (*Op)(CVal); };
static const struct mgrType_ mgr = { .Op = mgr_Op_stub_ };
void check_(void) {
mgr.Op(((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_1"})}, {"draft", ((CVal){.b = true})}}}));
mgr.Op(((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_2"})}}}));
}
