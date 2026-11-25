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
int main(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.a = (CVal[]){
        ((CVal){.m = (CKV[]){{"item", ((CVal){.s = "existing"})}}}),
        ((CVal){.s = "kept"}),
        // This comment trails the first pair.
    }}),
    ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"item", ((CVal){.s = "next"})}}}), ((CVal){.s = "also kept"})}}),
    // This comment describes the last pair.
    ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"item", ((CVal){.s = "last"})}}}), ((CVal){.s = "kept too"})}}),
}});
    (void)my_data;
    return 0;
}
