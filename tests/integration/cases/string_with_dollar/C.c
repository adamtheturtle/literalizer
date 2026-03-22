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
    ((_CVal){.s = "price $10"}),
    ((_CVal){.s = "$HOME"}),
}});
    (void)_v;
}
