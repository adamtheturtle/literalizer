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
static void obj_BEGIN_stub_(CVal _a0) { (void)_a0; }
struct objType_ { void (*BEGIN)(CVal); };
static const struct objType_ obj = { .BEGIN = obj_BEGIN_stub_ };
int main(void) {
obj.BEGIN(((CVal){.i = 42}));
    return 0;
}
