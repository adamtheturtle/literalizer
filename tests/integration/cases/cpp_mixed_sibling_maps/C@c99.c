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
    ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"a", ((CVal){.i = 1})}}}), ((CVal){.m = (CKV[]){{"a", ((CVal){.s = NULL})}}}), ((CVal){.i = 42})}}),
    ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"a", ((CVal){.i = 1})}}}), ((CVal){.m = (CKV[]){{"a", ((CVal){.s = "s"})}}}), ((CVal){.i = 42})}}),
    ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"a", ((CVal){.i = 1})}}}), ((CVal){.m = (CKV[]){{"a", ((CVal){.s = NULL})}}})}}),
    ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"a", ((CVal){.i = 1})}}}), ((CVal){.m = (CKV[]){{"a", ((CVal){.s = "s"})}}})}}),
}});
    (void)my_data;
    return 0;
}
