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
static void process(CVal _a0, CVal _a1, CVal _a2) { (void)_a0; (void)_a1; (void)_a2; }
int main(void) {
process(((CVal){.i = 1}), ((CVal){.i = 0}), ((CVal){.i = 3600}));  // Jan 1 1970 00:00:00 - 01:00:00
process(((CVal){.i = 5}), ((CVal){.i = 0}), ((CVal){.i = 3600}));  // Jan 1 1970 00:00:05 - 01:00:05
process(((CVal){.i = 2}), ((CVal){.i = 0}), ((CVal){.i = 5400}));  // Jan 1 1970 00:00:02 - 01:30:02
    return 0;
}
