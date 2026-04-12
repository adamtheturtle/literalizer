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
    ((CVal){.i = 0xf4240}),
    ((CVal){.i = -0x4d2}),
    ((CVal){.i = 0xff}),
    ((CVal){.i = -0xa}),
}});
    (void)my_data;
}
