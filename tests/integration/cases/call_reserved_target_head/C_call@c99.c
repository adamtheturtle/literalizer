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
static void class_member_stub_(CVal _a0) { (void)_a0; }
struct classType_ { void (*member)(CVal); };
static const struct classType_ class = { .member = class_member_stub_ };
int main(void) {
class.member(((CVal){.i = 42}));
    return 0;
}
