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
static void process(CVal _a0) { (void)_a0; }
int main(void) {
process(((CVal){.s = "09:30:00"}));
process(((CVal){.s = "2024-01-15T00:00:00+00:00"}));
process(((CVal){.i = 1}));
    return 0;
}
