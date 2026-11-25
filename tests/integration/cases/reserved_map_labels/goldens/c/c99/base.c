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
    {"if", ((CVal){.i = 1})},
    {"then", ((CVal){.i = 2})},
    {"else", ((CVal){.i = 3})},
    {"let", ((CVal){.i = 4})},
    {"in", ((CVal){.i = 5})},
    {"using", ((CVal){.i = 6})},
    {"missing", ((CVal){.i = 7})},
    {"assert", ((CVal){.i = 8})},
    {"as", ((CVal){.i = 9})},
    {"Infinity", ((CVal){.i = 10})},
    {"NaN", ((CVal){.i = 11})},
    {"merge", ((CVal){.i = 12})},
    {"Some", ((CVal){.i = 13})},
    {"toMap", ((CVal){.i = 14})},
    {"forall", ((CVal){.i = 15})},
    {"with", ((CVal){.i = 16})},
    {"ordinary", ((CVal){.i = 17})},
}});
    (void)my_data;
    return 0;
}
