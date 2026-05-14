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
static void process(CVal _a0) { (void)_a0; }
int main(void) {
// Test cases
process(((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_1"})}}}));  // first case
process(((CVal){.m = (CKV[]){{"type", ((CVal){.s = "update"})}, {"pr_id", ((CVal){.s = "pr_2"})}}}));  // second case
// third case
process(((CVal){.m = (CKV[]){{"type", ((CVal){.s = "delete"})}, {"pr_id", ((CVal){.s = "pr_3"})}}}));
    return 0;
}
