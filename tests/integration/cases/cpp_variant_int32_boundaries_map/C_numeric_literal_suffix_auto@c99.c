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
    {"below", ((CVal){.i = -2147483649L})},
    {"minimum", ((CVal){.i = -2147483648L})},
    {"above", ((CVal){.i = -2147483647L})},
    {"nested", ((CVal){.a = (CVal[]){((CVal){.i = 0L})}})},
}});
    (void)my_data;
    return 0;
}
