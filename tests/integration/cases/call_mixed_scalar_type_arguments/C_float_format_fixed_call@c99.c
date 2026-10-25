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
#include <math.h>
static void capture(CVal _a0, CVal _a1, CVal _a2, CVal _a3, CVal _a4, CVal _a5, CVal _a6) { (void)_a0, (void)_a1, (void)_a2, (void)_a3, (void)_a4, (void)_a5, (void)_a6; }
int main(void) {
capture(((CVal){.f = NAN}), ((CVal){.f = INFINITY}), ((CVal){.f = -INFINITY}), ((CVal){.f = 1.250000}), ((CVal){.s = "2024-01-15"}), ((CVal){.s = "2024-01-15T12:34:56"}), ((CVal){.s = "[ordinary text]"}));
    return 0;
}
