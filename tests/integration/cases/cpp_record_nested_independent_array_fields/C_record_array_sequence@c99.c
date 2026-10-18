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
struct Record0 { const CVal *numbers; const CVal *words; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .numbers = (CVal[]){
        ((CVal){.a = (CVal[]){
            ((CVal){.i = 1}),
        }}),
        ((CVal){.a = (CVal[]){
            ((CVal){.i = 2}),
        }}),
    },
    .words = (CVal[]){
        ((CVal){.a = (CVal[]){
            ((CVal){.s = "s"}),
        }}),
        ((CVal){.a = (CVal[]){
            ((CVal){.s = "t"}),
        }}),
    },
};
    (void)my_data;
    return 0;
}
