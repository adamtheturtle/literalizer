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
    {"positive", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"item", ((CVal){.a = (CVal[]){((CVal){.i = 2147483648})}})}}})}})},
    {"negative", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"item", ((CVal){.a = (CVal[]){((CVal){.i = -2147483649})}})}}})}})},
    {"mixed", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"item", ((CVal){.a = (CVal[]){((CVal){.i = 0}), ((CVal){.i = 2147483648})}})}}})}})},
}});
    (void)my_data;
    return 0;
}
