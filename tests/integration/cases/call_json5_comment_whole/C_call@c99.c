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
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(((CVal){.i = 42}));
    return 0;
}
