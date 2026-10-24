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
static void obj_class_stub_(CVal _a0) { (void)_a0; }
struct objType_ { void (*class)(CVal); };
static const struct objType_ obj = { .class = obj_class_stub_ };
int main(void) {
obj.class(((CVal){.i = 42}));
    return 0;
}
