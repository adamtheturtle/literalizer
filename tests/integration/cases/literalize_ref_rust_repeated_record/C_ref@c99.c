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
struct Record0 { const CVal *value; };
int main(void) {
struct Record0 shared = (struct Record0){
    .value = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    },
};
struct Record0 my_data[] = {
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
