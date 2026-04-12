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
    ((CVal){.b = true}),
    ((CVal){.s = "hi"}),
    ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.i = 2})}}),
    ((CVal){.s = NULL}),
}});
    (void)my_data;
}
