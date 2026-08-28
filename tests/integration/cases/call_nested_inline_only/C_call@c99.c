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
static void f(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; }
int main(void) {
f(((CVal){.i = 2}), ((CVal){.s = "hello"}));  // trailing note
f(((CVal){.i = 3}), ((CVal){.s = "world"}));  // another note
    return 0;
}
