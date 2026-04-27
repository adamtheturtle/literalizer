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
static void process(CVal _a0) { (void)_a0; }
void check_(void) {
CVal my_var = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
    ((CVal){.i = 3}),
}});
process(my_var);
}
