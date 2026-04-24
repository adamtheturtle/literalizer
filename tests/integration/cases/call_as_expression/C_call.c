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
CVal process(CVal, CVal);
void check_(void) {
CVal items = ((CVal){.a = (CVal[]){
    process(((CVal){.i = 1}), ((CVal){.i = 42})),
    process(((CVal){.i = 2}), ((CVal){.i = 100})),
}});
    (void)items;
}
