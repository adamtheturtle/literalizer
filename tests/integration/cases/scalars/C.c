#include <stdbool.h>
#include <stddef.h>
typedef struct _CVal _CVal;
typedef struct _CKV _CKV;
struct _CVal {
    union {
        _Bool b;
        long long i;
        double f;
        const char *s;
        const _CVal *a;
        const _CKV *m;
    };
};
struct _CKV { const char *k; _CVal v; };
void _check(void) {
    _CVal _v = ((_CVal){.a = (_CVal[]){
    ((_CVal){.i = 42}),
    ((_CVal){.f = 3.14}),
    ((_CVal){.b = true}),
    ((_CVal){.b = false}),
    ((_CVal){.s = "hello \"world\""}),
}});
    (void)_v;
}
