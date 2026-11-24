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
    {"i32_below", ((CVal){.i = -0x80000001LL})},
    {"i32_minimum", ((CVal){.i = -0x80000000LL})},
    {"i32_above", ((CVal){.i = -0x7fffffff})},
    {"i32_maximum", ((CVal){.i = 0x7fffffff})},
    {"i32_over", ((CVal){.i = 0x80000000})},
    {"i64_minimum", ((CVal){.i = (-9223372036854775807LL - 1)})},
    {"i64_maximum", ((CVal){.i = 0x7fffffffffffffff})},
}});
    (void)my_data;
    return 0;
}
