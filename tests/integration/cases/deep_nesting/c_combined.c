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
    {"level1", ((_CVal){.m = (_CKV[]){{"level2", ((_CVal){.m = (_CKV[]){{"level3", ((_CVal){.m = (_CKV[]){{"level4", ((_CVal){.m = (_CKV[]){{"value", ((_CVal){.s = "deep"})}, {"items", ((_CVal){.a = (_CVal[]){((_CVal){.s = "a"}), ((_CVal){.s = "b"})}})}}})}}})}, {"sibling", ((_CVal){.i = 42})}}})}, {"tags", ((_CVal){.a = (_CVal[]){((_CVal){.m = (_CKV[]){{"name", ((_CVal){.s = "tag1"})}, {"meta", ((_CVal){.m = (_CKV[]){{"priority", ((_CVal){.i = 1})}, {"labels", ((_CVal){.a = (_CVal[]){((_CVal){.s = "x"}), ((_CVal){.s = "y"})}})}}})}}})}})}}})},
}});
my_data = ((_CVal){.m = (_CKV[]){
    {"level1", ((_CVal){.m = (_CKV[]){{"level2", ((_CVal){.m = (_CKV[]){{"level3", ((_CVal){.m = (_CKV[]){{"level4", ((_CVal){.m = (_CKV[]){{"value", ((_CVal){.s = "deep"})}, {"items", ((_CVal){.a = (_CVal[]){((_CVal){.s = "a"}), ((_CVal){.s = "b"})}})}}})}}})}, {"sibling", ((_CVal){.i = 42})}}})}, {"tags", ((_CVal){.a = (_CVal[]){((_CVal){.m = (_CKV[]){{"name", ((_CVal){.s = "tag1"})}, {"meta", ((_CVal){.m = (_CKV[]){{"priority", ((_CVal){.i = 1})}, {"labels", ((_CVal){.a = (_CVal[]){((_CVal){.s = "x"}), ((_CVal){.s = "y"})}})}}})}}})}})}}})},
}});
    (void)my_data;
}
