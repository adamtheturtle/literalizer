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
static CVal a_foo_Foo_bar_stub_(CVal _a0) { (void)_a0; return (CVal){0}; }
struct FooType_ { CVal (*bar)(CVal); };
struct fooType_ { struct FooType_ Foo; };
struct aType_ { struct fooType_ foo; };
static const struct aType_ a = { .foo = { .Foo = { .bar = a_foo_Foo_bar_stub_ } } };
int main(void) {
CVal my_data = a.foo.Foo.bar(((CVal){.a = (CVal[]){((CVal){.i = 1})}}));
    (void)my_data;
    return 0;
}
