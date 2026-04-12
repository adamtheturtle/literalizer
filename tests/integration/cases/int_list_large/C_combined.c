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
    ((CVal){.i = 1000000}),
    ((CVal){.i = -1234}),
    ((CVal){.i = 255}),
    ((CVal){.i = -10}),
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1000000}),
    ((CVal){.i = -1234}),
    ((CVal){.i = 255}),
    ((CVal){.i = -10}),
}});
    (void)my_data;
}
