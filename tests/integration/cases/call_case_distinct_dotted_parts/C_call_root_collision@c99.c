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
static void foo_Foo_bar_stub_(CVal _a0) { (void)_a0; }
struct FooType_ { void (*bar)(CVal); };
struct fooType_ { struct FooType_ Foo; };
static const struct fooType_ foo = { .Foo = { .bar = foo_Foo_bar_stub_ } };
int main(void) {
foo.Foo.bar(((CVal){.a = (CVal[]){((CVal){.i = 1})}}));
    return 0;
}
