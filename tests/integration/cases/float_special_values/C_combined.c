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
#include <math.h>
void _check(void) {
_CVal my_data = ((_CVal){.a = (_CVal[]){
    ((_CVal){.f = INFINITY}),
    ((_CVal){.f = -INFINITY}),
    ((_CVal){.f = NAN}),
}});
my_data = ((_CVal){.a = (_CVal[]){
    ((_CVal){.f = INFINITY}),
    ((_CVal){.f = -INFINITY}),
    ((_CVal){.f = NAN}),
}});
    (void)my_data;
}
