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
    {"1", ((CVal){.s = "one"})},
    {"2", ((CVal){.s = "two"})},
    {"42", ((CVal){.s = "answer"})},
}});
    (void)my_data;
}
