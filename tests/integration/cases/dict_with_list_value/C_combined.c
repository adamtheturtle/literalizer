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
    {"scores", ((_CVal){.a = (_CVal[]){((_CVal){.i = 10}), ((_CVal){.i = 20}), ((_CVal){.i = 30})}})},
}});
my_data = ((_CVal){.m = (_CKV[]){
    {"name", ((_CVal){.s = "Alice"})},
    {"scores", ((_CVal){.a = (_CVal[]){((_CVal){.i = 10}), ((_CVal){.i = 20}), ((_CVal){.i = 30})}})},
}});
    (void)my_data;
}
