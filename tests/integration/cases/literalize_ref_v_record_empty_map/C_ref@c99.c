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
struct Record0 { CVal bound; };
int main(void) {
CVal empty_map = ((CVal){.m = (CKV[]){}});
struct Record0 my_data = (struct Record0){
    .bound = empty_map,
};
    (void)my_data;
    return 0;
}
