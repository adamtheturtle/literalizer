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
CVal deep = ((CVal){.m = (CKV[]){
    {"_", ((CVal){.s = "_"})},
}});
CVal my_data = ((CVal){.m = (CKV[]){
    {"a", ((CVal){.m = (CKV[]){{"b", ((CVal){.m = (CKV[]){{"c", deep}}})}}})},
}});
    (void)my_data;
    return 0;
}
