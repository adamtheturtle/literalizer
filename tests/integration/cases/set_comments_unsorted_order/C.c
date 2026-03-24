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
    // before apple
    ((_CVal){.s = "apple"}),
    ((_CVal){.s = "banana"}),  // banana inline
    // trailing
}});
    (void)my_data;
}
