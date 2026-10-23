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
static void check(CVal _a0, CVal _a1) { (void)_a0, (void)_a1; }
int main(void) {
check(((CVal){.s = "2024-01-15T10:30:00+00:00"}), ((CVal){.s = "2024-06-01"}));
    return 0;
}
