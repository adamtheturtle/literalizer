#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
static int throttler_check_stub_() { return 0; }
struct throttlerType_ { int (*check)(); };
static const struct throttlerType_ throttler = { .check = throttler_check_stub_ };
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
void emit();
void check_(void) {
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
}
