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
    {"s", ((CVal){.s = "string"})},
    {"i", ((CVal){.i = 1})},
    {"f", ((CVal){.f = 1.5})},
    {"b", ((CVal){.b = true})},
    {"n", ((CVal){.s = NULL})},
    {"d", ((CVal){.s = "2024-01-15"})},
    {"dt", ((CVal){.s = "2024-01-15T12:00:00"})},
    {"by", ((CVal){.s = "48656c6c6f"})},
}});
    (void)my_data;
    return 0;
}
