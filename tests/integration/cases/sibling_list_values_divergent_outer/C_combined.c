#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
void check_(void) {
CVal my_data = ((CVal){.m = (CKV[]){
    {"a", ((CVal){.a = (CVal[]){((CVal){.i = 1})}})},
    {"b", ((CVal){.a = (CVal[]){((CVal){.s = "x"})}})},
}});
my_data = ((CVal){.m = (CKV[]){
    {"a", ((CVal){.a = (CVal[]){((CVal){.i = 1})}})},
    {"b", ((CVal){.a = (CVal[]){((CVal){.s = "x"})}})},
}});
    (void)my_data;
}
