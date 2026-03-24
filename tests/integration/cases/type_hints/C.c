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
    _CVal my_data = ((_CVal){.m = (_CKV[]){
    {"name", ((_CVal){.s = "Alice"})},
    {"age", ((_CVal){.i = 30})},
    {"active", ((_CVal){.b = true})},
    {"score", ((_CVal){.s = NULL})},
    {"joined", ((_CVal){.s = "2024-01-15"})},
    {"last_login", ((_CVal){.s = "2024-01-15T12:30:00+00:00"})},
    {"avatar", ((_CVal){.s = "48656c6c6f"})},
}});
    (void)my_data;
}
