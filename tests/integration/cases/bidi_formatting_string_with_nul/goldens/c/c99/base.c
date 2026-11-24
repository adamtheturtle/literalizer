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
    {"v", ((CVal){.s = (const char[]){'\141', '\342', '\200', '\252', '\000', '\303', '\251', '\360', '\237', '\230', '\200', '\142', '\000'}})},
}});
    (void)my_data;
    return 0;
}
