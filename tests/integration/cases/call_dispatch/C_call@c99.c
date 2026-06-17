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
static void put(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; }
static void get(CVal _a0) { (void)_a0; }
int main(void) {
put(((CVal){.i = 1}), ((CVal){.i = 10}));
get(((CVal){.i = 1}));
    return 0;
}
