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
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"a", ((CVal){.i = 1L})}}}),
    ((CVal){.i = 1L}),
    ((CVal){.s = "x"}),
    ((CVal){.b = true}),
    ((CVal){.f = 2.5}),
    ((CVal){.s = NULL}),
}});
    (void)my_data;
    return 0;
}
