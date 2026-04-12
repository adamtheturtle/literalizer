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
void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"x", ((CVal){.i = 1})}, {"y", ((CVal){.f = 2.5})}}}),
    ((CVal){.m = (CKV[]){{"x", ((CVal){.i = 3})}, {"y", ((CVal){.f = 4.0})}}}),
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"x", ((CVal){.i = 1})}, {"y", ((CVal){.f = 2.5})}}}),
    ((CVal){.m = (CKV[]){{"x", ((CVal){.i = 3})}, {"y", ((CVal){.f = 4.0})}}}),
}});
    (void)my_data;
}
