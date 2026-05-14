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
static void process(CVal _a0, CVal _a1, CVal _a2, CVal _a3) { (void)_a0; (void)_a1; (void)_a2; (void)_a3; }
int main(void) {
process(((CVal){.i = 1}), ((CVal){.i = 2}), ((CVal){.i = 3}), ((CVal){.i = 4}));
process(((CVal){.i = 5}), ((CVal){.i = 6}), ((CVal){.i = 7}), ((CVal){.i = 8}));
    return 0;
}
