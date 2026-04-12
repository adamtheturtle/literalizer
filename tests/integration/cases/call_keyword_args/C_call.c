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
void check_(void) {
struct _throttler_t { int (*check)(); };
struct _throttler_t throttler;
int print();
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
    (void)my_data;
}
