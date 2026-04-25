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
void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.a = (CVal[]){((CVal){.s = "2026-01-01"}), ((CVal){.s = "2026-01-02"})}}),
    ((CVal){.a = (CVal[]){}}),
    ((CVal){.a = (CVal[]){((CVal){.s = "2026-02-03"}), ((CVal){.s = "2026-02-04"})}}),
}});
    (void)my_data;
}
