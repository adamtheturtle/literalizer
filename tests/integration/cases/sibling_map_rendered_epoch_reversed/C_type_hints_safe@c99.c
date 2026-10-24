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
    {"b", ((CVal){.m = (CKV[]){{"k", ((CVal){.i = 1})}}})},
    {"a", ((CVal){.m = (CKV[]){{"k", ((CVal){.s = "2040-01-01T00:00:00+00:00"})}}})},
}});
    (void)my_data;
    return 0;
}
