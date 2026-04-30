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
CVal ref_x = ((CVal){.m = (CKV[]){
    {"_", ((CVal){.s = "_"})},
}});
CVal my_data = ((CVal){.a = (CVal[]){
    ref_x,
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
}});
    (void)my_data;
    return 0;
}
