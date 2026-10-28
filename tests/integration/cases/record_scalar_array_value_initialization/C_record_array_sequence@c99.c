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
struct Record0 { const CVal *numbers; const CVal *nested_numbers; const CVal *words; bool flag; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .numbers = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    },
    .nested_numbers = (CVal[]){
        ((CVal){.a = (CVal[]){
            ((CVal){.i = 3}),
            ((CVal){.i = 4}),
        }}),
        ((CVal){.a = (CVal[]){
            ((CVal){.i = 5}),
            ((CVal){.i = 6}),
        }}),
    },
    .words = (CVal[]){
        ((CVal){.s = "s"}),
    },
    .flag = true,
};
    (void)my_data;
    return 0;
}
