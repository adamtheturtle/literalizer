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
CVal sibling_map = ((CVal){.m = (CKV[]){
    {"k", ((CVal){.i = 2})},
}});
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"k", ((CVal){.i = 1})}}}),
    sibling_map,
}});
    (void)my_data;
    return 0;
}
