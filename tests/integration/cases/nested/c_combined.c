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
    {"users", ((_CVal){.a = (_CVal[]){((_CVal){.m = (_CKV[]){{"name", ((_CVal){.s = "Bob"})}, {"tags", ((_CVal){.a = (_CVal[]){((_CVal){.s = "admin"}), ((_CVal){.s = "user"})}})}}}), ((_CVal){.m = (_CKV[]){{"name", ((_CVal){.s = "Carol"})}, {"tags", ((_CVal){.a = (_CVal[]){((_CVal){.s = "guest"})}})}}})}})},
}});
my_data = ((_CVal){.m = (_CKV[]){
    {"users", ((_CVal){.a = (_CVal[]){((_CVal){.m = (_CKV[]){{"name", ((_CVal){.s = "Bob"})}, {"tags", ((_CVal){.a = (_CVal[]){((_CVal){.s = "admin"}), ((_CVal){.s = "user"})}})}}}), ((_CVal){.m = (_CKV[]){{"name", ((_CVal){.s = "Carol"})}, {"tags", ((_CVal){.a = (_CVal[]){((_CVal){.s = "guest"})}})}}})}})},
}});
    (void)my_data;
}
