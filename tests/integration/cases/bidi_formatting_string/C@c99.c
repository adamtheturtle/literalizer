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
    {"v", ((CVal){.s = (const char[]){'\141', '\342', '\200', '\252', '\342', '\200', '\253', '\342', '\200', '\254', '\342', '\200', '\255', '\342', '\200', '\256', '\342', '\201', '\246', '\342', '\201', '\247', '\342', '\201', '\250', '\342', '\201', '\251', '\142', '\000'}})},
}});
    (void)my_data;
    return 0;
}
