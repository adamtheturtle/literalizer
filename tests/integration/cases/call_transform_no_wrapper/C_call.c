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
static CVal process(CVal _a0) { (void)_a0; return (CVal){0}; }
void check_(void) {
process(((CVal){.s = "hello"}));
process(((CVal){.i = 42}));
process(((CVal){.b = true}));
}
