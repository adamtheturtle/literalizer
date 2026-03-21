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
    ((_CVal){.s = "2024-01-15T12:30:00+00:00"}),
    ((_CVal){.s = "2024-06-30T08:00:00+00:00"}),
    ((_CVal){.s = "2024-12-25T18:45:00+00:00"}),
}});
my_data = ((_CVal){.a = (_CVal[]){
    ((_CVal){.s = "2024-01-15T12:30:00+00:00"}),
    ((_CVal){.s = "2024-06-30T08:00:00+00:00"}),
    ((_CVal){.s = "2024-12-25T18:45:00+00:00"}),
}});
    (void)my_data;
}
