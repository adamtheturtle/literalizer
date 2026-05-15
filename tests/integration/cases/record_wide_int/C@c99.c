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
    {"quantity", ((CVal){.i = 1000000})},
    {"big", ((CVal){.u = 18446744073709551615ULL})},
    {"ratio", ((CVal){.f = 2.5})},
    {"label", ((CVal){.s = "tag"})},
    {"ok", ((CVal){.b = true})},
}});
    (void)my_data;
    return 0;
}
