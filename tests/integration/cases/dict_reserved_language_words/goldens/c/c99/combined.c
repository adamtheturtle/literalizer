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
    {"assert", ((CVal){.i = 1})},
    {"else", ((CVal){.i = 1})},
    {"error", ((CVal){.i = 1})},
    {"false", ((CVal){.i = 1})},
    {"for", ((CVal){.i = 1})},
    {"function", ((CVal){.i = 1})},
    {"if", ((CVal){.i = 1})},
    {"import", ((CVal){.i = 1})},
    {"importbin", ((CVal){.i = 1})},
    {"importstr", ((CVal){.i = 1})},
    {"in", ((CVal){.i = 1})},
    {"local", ((CVal){.i = 1})},
    {"null", ((CVal){.i = 1})},
    {"self", ((CVal){.i = 1})},
    {"super", ((CVal){.i = 1})},
    {"tailstrict", ((CVal){.i = 1})},
    {"then", ((CVal){.i = 1})},
    {"true", ((CVal){.i = 1})},
    {"ordinary", ((CVal){.i = 1})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"assert", ((CVal){.i = 1})},
    {"else", ((CVal){.i = 1})},
    {"error", ((CVal){.i = 1})},
    {"false", ((CVal){.i = 1})},
    {"for", ((CVal){.i = 1})},
    {"function", ((CVal){.i = 1})},
    {"if", ((CVal){.i = 1})},
    {"import", ((CVal){.i = 1})},
    {"importbin", ((CVal){.i = 1})},
    {"importstr", ((CVal){.i = 1})},
    {"in", ((CVal){.i = 1})},
    {"local", ((CVal){.i = 1})},
    {"null", ((CVal){.i = 1})},
    {"self", ((CVal){.i = 1})},
    {"super", ((CVal){.i = 1})},
    {"tailstrict", ((CVal){.i = 1})},
    {"then", ((CVal){.i = 1})},
    {"true", ((CVal){.i = 1})},
    {"ordinary", ((CVal){.i = 1})},
}});
    (void)my_data;
    return 0;
}
