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
    ((CVal){.m = (CKV[]){{"item", ((CVal){.s = "existing"})}}}),
    // This comment describes the next item.
    ((CVal){.m = (CKV[]){{"item", ((CVal){.s = "next"})}}}),
}});
(void)my_data;
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"item", ((CVal){.s = "existing"})}}}),
    // This comment describes the next item.
    ((CVal){.m = (CKV[]){{"item", ((CVal){.s = "next"})}}}),
}});
    (void)my_data;
    return 0;
}
