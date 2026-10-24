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
static void obj_ZKV_stub_(CVal _a0) { (void)_a0; }
struct objType_ { void (*ZKV)(CVal); };
static const struct objType_ obj = { .ZKV = obj_ZKV_stub_ };
int main(void) {
obj.ZKV(((CVal){.i = 1}));
    return 0;
}
