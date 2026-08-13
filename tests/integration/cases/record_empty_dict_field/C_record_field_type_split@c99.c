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
struct Record0 { CVal f; long long g; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .f = ((CVal){.m = (CKV[]){}}),
    .g = 1,
};
    (void)my_data;
    return 0;
}
