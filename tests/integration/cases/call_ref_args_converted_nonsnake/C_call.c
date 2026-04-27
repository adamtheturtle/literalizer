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
static void process(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; }
void check_(void) {
CVal my_var = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
    ((CVal){.i = 3}),
}});
CVal my_other = ((CVal){.a = (CVal[]){
    ((CVal){.i = 4}),
    ((CVal){.i = 5}),
    ((CVal){.i = 6}),
}});
process(my_var, ((CVal){.i = 42}));
process(my_other, ((CVal){.i = 7}));
}
