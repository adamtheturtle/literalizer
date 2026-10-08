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
struct Record1 { const CVal *values; };
struct Record2 { const CVal *nested; };
struct Record0 { struct Record1 trivial; struct Record2 nested; };
int main(void) {
struct Record1 trivial = (struct Record1){
    .values = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    },
};
struct Record2 nested = (struct Record2){
    .nested = (CVal[]){
        ((CVal){.a = (CVal[]){
            ((CVal){.i = 1}),
            ((CVal){.i = 2}),
        }}),
        ((CVal){.a = (CVal[]){
            ((CVal){.i = 3}),
            ((CVal){.i = 4}),
        }}),
    },
};
struct Record0 my_data = (struct Record0){
    .trivial = trivial,
    .nested = nested,
};
    (void)my_data;
    return 0;
}
