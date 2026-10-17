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
static void thing_Before_stub_(CVal _a0) { (void)_a0; }
struct thingType_ { void (*Before)(CVal); };
static const struct thingType_ thing = { .Before = thing_Before_stub_ };
int main(void) {
thing.Before(((CVal){.i = 1}));
    return 0;
}
