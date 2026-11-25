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
CVal my_data = ((CVal){.m = (CKV[]){
    {"items", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"id", ((CVal){.i = 1})}}}), ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 2})}, {"count", ((CVal){.i = 10})}}}), ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 3})}, {"count", ((CVal){.i = 20})}}})}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"items", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"id", ((CVal){.i = 1})}}}), ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 2})}, {"count", ((CVal){.i = 10})}}}), ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 3})}, {"count", ((CVal){.i = 20})}}})}})},
}});
    (void)my_data;
    return 0;
}
