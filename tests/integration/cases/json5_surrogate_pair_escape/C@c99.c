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
    {"astral", ((CVal){.s = "😀"})},
    {"mixed", ((CVal){.s = "a😀b"})},
    {"count", ((CVal){.i = 2})},
    {"list", ((CVal){.a = (CVal[]){((CVal){.s = "😀"}), ((CVal){.i = 1})}})},
    {"nested", ((CVal){.m = (CKV[]){{"inner", ((CVal){.s = "😀"})}}})},
}});
    (void)my_data;
    return 0;
}
