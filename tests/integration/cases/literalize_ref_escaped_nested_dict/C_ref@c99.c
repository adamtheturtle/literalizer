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
CVal existing = ((CVal){.i = 1});
CVal my_data = ((CVal){.m = (CKV[]){
    {"nested", ((CVal){.a = (CVal[]){((CVal){.i = 0}), existing}})},
}});
    (void)my_data;
    return 0;
}
