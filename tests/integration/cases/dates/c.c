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
    _CVal _v = ((_CVal){.m = (_CKV[]){
    {"date", ((_CVal){.s = "2024-01-15"})},
    {"datetime", ((_CVal){.s = "2024-01-15T12:30:00+00:00"})},
}});
    (void)_v;
}
