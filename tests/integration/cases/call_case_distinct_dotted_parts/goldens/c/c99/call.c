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
static void a_foo_Foo_bar_stub_(CVal _a0) { (void)_a0; }
struct FooType_ { void (*bar)(CVal); };
struct fooType_ { struct FooType_ Foo; };
struct aType_ { struct fooType_ foo; };
static const struct aType_ a = { .foo = { .Foo = { .bar = a_foo_Foo_bar_stub_ } } };
int main(void) {
a.foo.Foo.bar(((CVal){.a = (CVal[]){((CVal){.i = 1})}}));
    return 0;
}
