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
int main(void) {
CVal my_var = ((CVal){.i = 42});
process(((CVal){.m = (CKV[]){{"key", my_var}, {"count", ((CVal){.i = 42})}, {"label", ((CVal){.s = "example"})}}}));
    return 0;
}
