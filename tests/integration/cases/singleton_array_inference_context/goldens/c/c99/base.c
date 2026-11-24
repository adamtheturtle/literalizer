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
    {"nil", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.s = NULL})}})}})}})}})}})}})}})}})}})},
    {"empty", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){}})}})}})}})}})}})}})}})}})}})},
    {"siblings", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.i = 4}), ((CVal){.i = 5})}})}})}})}})}})}})}})}})}})}})},
}});
    (void)my_data;
    return 0;
}
