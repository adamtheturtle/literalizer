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
static CVal process(CVal _a0) { (void)_a0; return (CVal){0}; }
static void helpers_emit_stub_(CVal _a0, CVal _a1) { (void)_a0, (void)_a1; }
struct helpersType_ { void (*emit)(CVal, CVal); };
static const struct helpersType_ helpers = { .emit = helpers_emit_stub_ };
int main(void) {
helpers.emit(process(((CVal){.i = 1})), ((CVal){.i = 42}));
    return 0;
}
