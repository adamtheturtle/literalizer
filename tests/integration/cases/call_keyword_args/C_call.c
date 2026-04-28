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
static CVal throttler_check_stub_(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; return (CVal){0}; }
struct throttlerType_ { CVal (*check)(CVal, CVal); };
static const struct throttlerType_ throttler = { .check = throttler_check_stub_ };
static void emit(CVal _a0) { (void)_a0; }
int main(void) {
emit(throttler.check(((CVal){.s = "user_1"}), ((CVal){.f = 1000.0})));
emit(throttler.check(((CVal){.s = "user_2"}), ((CVal){.f = 2000.5})));
    return 0;
}
