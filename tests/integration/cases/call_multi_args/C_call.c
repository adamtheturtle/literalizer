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
void process(CVal, CVal);
void check_(void) {
process(((CVal){.i = 1}), ((CVal){.i = 42}));
process(((CVal){.i = 2}), ((CVal){.i = 100}));
}
