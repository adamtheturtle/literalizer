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
    _CVal my_data = ((_CVal){.a = (_CVal[]){
    ((_CVal){.a = (_CVal[]){((_CVal){.f = 1.5}), ((_CVal){.f = 2.5})}}),
    ((_CVal){.a = (_CVal[]){((_CVal){.f = 3.5}), ((_CVal){.f = 4.5})}}),
}});
    (void)my_data;
}
