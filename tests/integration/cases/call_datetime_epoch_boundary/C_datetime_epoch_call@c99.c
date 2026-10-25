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
static void consume(CVal _a0) { (void)_a0; }
int main(void) {
consume(((CVal){.i = -2147483649}));
consume(((CVal){.i = 2147483648}));
    return 0;
}
