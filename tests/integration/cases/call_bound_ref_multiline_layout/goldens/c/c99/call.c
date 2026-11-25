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
static void f(CVal _a0) { (void)_a0; }
int main(void) {
CVal ref_data = ((CVal){.a = (CVal[]){
    ((CVal){.a = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    }}),
    ((CVal){.a = (CVal[]){
        ((CVal){.i = 3}),
        ((CVal){.i = 4}),
    }}),
}});
f(((CVal){.a = (CVal[]){
    ((CVal){.a = (CVal[]){
        ref_data,
    }}),
}}));
    return 0;
}
