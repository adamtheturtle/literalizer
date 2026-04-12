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
    {"key\nwith\nnewlines", ((CVal){.s = "value1"})},
    {"key\twith\ttabs", ((CVal){.s = "value2"})},
    {"", ((CVal){.s = "value3"})},
}});
    (void)my_data;
}
