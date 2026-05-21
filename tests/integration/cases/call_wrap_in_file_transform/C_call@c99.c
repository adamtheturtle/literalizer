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
static CVal process(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; return (CVal){0}; }
int main(void) {
CVal my_data = process(((CVal){.i = 1}), ((CVal){.i = 2}));
    (void)my_data;
    return 0;
}
