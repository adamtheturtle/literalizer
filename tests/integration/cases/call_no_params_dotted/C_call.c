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
static void throttler_check_stub_(void) {}
struct throttlerType_ { void (*check)(void); };
static const struct throttlerType_ throttler = { .check = throttler_check_stub_ };
int main(void) {
throttler.check();
throttler.check();
    return 0;
}
