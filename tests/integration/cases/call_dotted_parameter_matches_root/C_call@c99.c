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
static void outer_inner_stub_(CVal _a0, CVal _a1) { (void)_a0, (void)_a1; }
struct outerType_ { void (*inner)(CVal, CVal); };
static const struct outerType_ outer = { .inner = outer_inner_stub_ };
int main(void) {
outer.inner(((CVal){.i = 1}), ((CVal){.i = 2}));
    return 0;
}
