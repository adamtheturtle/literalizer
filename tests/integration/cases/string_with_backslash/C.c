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
    ((_CVal){.s = "C:\\path\\to\\file"}),
    ((_CVal){.s = "back\\\\slash"}),
    ((_CVal){.s = "hello \\\"world\\\""}),
    ((_CVal){.s = "path\\to \"# file"}),
    ((_CVal){.s = "trailing\\"}),
    ((_CVal){.s = "both \"quotes''' here"}),
}});
    (void)my_data;
}
