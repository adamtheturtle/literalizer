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
static void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.a = (CVal[]){((CVal){.f = 1.500000}), ((CVal){.f = 2.500000})}}),
    ((CVal){.a = (CVal[]){((CVal){.f = 3.500000}), ((CVal){.f = 4.500000})}}),
}});
    (void)my_data;
}
