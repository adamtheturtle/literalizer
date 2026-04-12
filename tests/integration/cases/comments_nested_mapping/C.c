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
CVal my_data = ((CVal){.m = (CKV[]){
    {"a", ((CVal){.m = (CKV[]){{"x", ((CVal){.i = 1})}}})},
    {"b", ((CVal){.i = 2})},
}});
    (void)my_data;
}
