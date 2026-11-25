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
struct Record0 { const CVal *flags; const CVal *values; const CVal *ints; const CVal *text; const CVal *nested_flags; const CVal *nested_values; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .flags = (CVal[]){
        ((CVal){.b = true}),
        ((CVal){.b = false}),
    },
    .values = (CVal[]){
        ((CVal){.f = 1.5}),
        ((CVal){.f = -2.25}),
    },
    .ints = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    },
    .text = (CVal[]){
        ((CVal){.s = "a"}),
    },
    .nested_flags = (CVal[]){
        ((CVal){.a = (CVal[]){
            ((CVal){.b = true}),
        }}),
        ((CVal){.a = (CVal[]){
            ((CVal){.b = false}),
        }}),
    },
    .nested_values = (CVal[]){
        ((CVal){.a = (CVal[]){
            ((CVal){.f = 1.5}),
        }}),
        ((CVal){.a = (CVal[]){
            ((CVal){.f = 2.25}),
        }}),
    },
};
    (void)my_data;
    return 0;
}
