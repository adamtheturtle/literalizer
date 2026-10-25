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
    {"del", ((CVal){.s = "ab"})},
    {"nel", ((CVal){.s = "ab"})},
    {"c1", ((CVal){.s = "ab"})},
}});
    (void)my_data;
    return 0;
}
