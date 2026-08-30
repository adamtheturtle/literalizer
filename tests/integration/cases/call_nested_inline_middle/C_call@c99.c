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
f(((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.s = "DEL"}), ((CVal){.s = "b"}), ((CVal){.s = "10"})}}), ((CVal){.a = (CVal[]){((CVal){.s = "ADD"}), ((CVal){.s = "a"}), ((CVal){.s = "x"})}})}}));  // note
// next call
f(((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.s = "ADD"}), ((CVal){.s = "c"}), ((CVal){.s = "y"})}})}}));
    return 0;
}
