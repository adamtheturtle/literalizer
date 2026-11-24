#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        unsigned long long u;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
int main(void) {
CVal my_data = ((CVal){.m = (CKV[]){
    {"level1", ((CVal){.m = (CKV[]){{"level2", ((CVal){.m = (CKV[]){{"level3", ((CVal){.m = (CKV[]){{"level4", ((CVal){.m = (CKV[]){{"value", ((CVal){.s = "deep"})}, {"items", ((CVal){.a = (CVal[]){((CVal){.s = "a"}), ((CVal){.s = "b"})}})}}})}}})}, {"sibling", ((CVal){.i = 42})}}})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "tag1"})}, {"meta", ((CVal){.m = (CKV[]){{"priority", ((CVal){.i = 1})}, {"labels", ((CVal){.a = (CVal[]){((CVal){.s = "x"}), ((CVal){.s = "y"})}})}}})}}})}})}}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"level1", ((CVal){.m = (CKV[]){{"level2", ((CVal){.m = (CKV[]){{"level3", ((CVal){.m = (CKV[]){{"level4", ((CVal){.m = (CKV[]){{"value", ((CVal){.s = "deep"})}, {"items", ((CVal){.a = (CVal[]){((CVal){.s = "a"}), ((CVal){.s = "b"})}})}}})}}})}, {"sibling", ((CVal){.i = 42})}}})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "tag1"})}, {"meta", ((CVal){.m = (CKV[]){{"priority", ((CVal){.i = 1})}, {"labels", ((CVal){.a = (CVal[]){((CVal){.s = "x"}), ((CVal){.s = "y"})}})}}})}}})}})}}})},
}});
    (void)my_data;
    return 0;
}
