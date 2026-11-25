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
    // A JSONC input case with both comment forms.
    {"url", ((CVal){.s = "https://example.org/a/*b*/"})},  // detail
    // continued
    {"count", ((CVal){.i = 0x2})},  // trailing line comment
}});
    (void)my_data;
    return 0;
}
