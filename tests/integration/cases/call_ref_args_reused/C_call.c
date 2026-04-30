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
static void process(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; }
int main(void) {
CVal shared = ((CVal){.i = 1});
CVal other = ((CVal){.i = 2});
process(shared, ((CVal){.i = 1}));
process(other, ((CVal){.i = 0}));
process(shared, ((CVal){.i = 8}));
    return 0;
}
