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
    {"lint", ((CVal){.a = (CVal[]){((CVal){.i = 2}), ((CVal){.a = (CVal[]){}})}})},
    {"test", ((CVal){.a = (CVal[]){((CVal){.i = 5}), ((CVal){.a = (CVal[]){((CVal){.s = "compile"})}})}})},
}});
    (void)my_data;
    return 0;
}
