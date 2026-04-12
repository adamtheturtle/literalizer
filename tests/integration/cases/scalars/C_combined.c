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
    ((CVal){.i = 42}),
    ((CVal){.f = 3.14}),
    ((CVal){.b = true}),
    ((CVal){.b = false}),
    ((CVal){.s = "hello \"world\""}),
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.i = 42}),
    ((CVal){.f = 3.14}),
    ((CVal){.b = true}),
    ((CVal){.b = false}),
    ((CVal){.s = "hello \"world\""}),
}});
    (void)my_data;
}
