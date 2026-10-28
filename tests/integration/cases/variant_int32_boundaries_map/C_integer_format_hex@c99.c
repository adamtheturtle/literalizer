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
    {"below", ((CVal){.i = -0x80000001LL})},
    {"minimum", ((CVal){.i = -0x80000000LL})},
    {"above", ((CVal){.i = -0x7fffffff})},
    {"nested", ((CVal){.a = (CVal[]){((CVal){.i = 0x0})}})},
}});
    (void)my_data;
    return 0;
}
