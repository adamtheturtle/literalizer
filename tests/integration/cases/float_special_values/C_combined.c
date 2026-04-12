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
#include <math.h>
static void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.f = INFINITY}),
    ((CVal){.f = -INFINITY}),
    ((CVal){.f = NAN}),
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.f = INFINITY}),
    ((CVal){.f = -INFINITY}),
    ((CVal){.f = NAN}),
}});
    (void)my_data;
}
