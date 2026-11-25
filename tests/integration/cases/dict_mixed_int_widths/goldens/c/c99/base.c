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
    {"a", ((CVal){.i = 1})},
    {"b", ((CVal){.i = 3000000000})},
    {"c", ((CVal){.s = "x"})},
}});
    (void)my_data;
    return 0;
}
