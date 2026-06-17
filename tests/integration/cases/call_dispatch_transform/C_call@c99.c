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
static CVal record(CVal _a0) { (void)_a0; return (CVal){0}; }
static void flush(CVal _a0) { (void)_a0; }
int main(void) {
record(((CVal){.i = 42}));
flush(((CVal){.i = 3}));
    return 0;
}
