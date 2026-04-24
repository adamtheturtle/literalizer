#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        unsigned long long u;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
void check_(void) {
CVal my_data = ((CVal){.m = (CKV[]){
    {"a", ((CVal){.s = NULL})},
    {"b", ((CVal){.s = NULL})},
    // trailing
}});
my_data = ((CVal){.m = (CKV[]){
    {"a", ((CVal){.s = NULL})},
    {"b", ((CVal){.s = NULL})},
    // trailing
}});
    (void)my_data;
}
