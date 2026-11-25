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
struct Record1 { const CVal *items; };
struct Record0 { struct Record1 outer; };
int main(void) {
struct Record1 record_data = (struct Record1){
    .items = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    },
};
struct Record0 my_data = (struct Record0){
    .outer = record_data,
};
    (void)my_data;
    return 0;
}
