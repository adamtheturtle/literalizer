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
struct CKV { const char *k; CVal v; };  // NOLINT(altera-struct-pack-align)
static void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.f = 0.0}),
    ((CVal){.f = 1.0}),
    ((CVal){.f = 1500.0}),
    ((CVal){.f = 0.001}),
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.f = 0.0}),
    ((CVal){.f = 1.0}),
    ((CVal){.f = 1500.0}),
    ((CVal){.f = 0.001}),
}});
    (void)my_data;
}
