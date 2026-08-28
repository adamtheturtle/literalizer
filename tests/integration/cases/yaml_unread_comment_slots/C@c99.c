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
    {"flow", ((CVal){.a = (CVal[]){
        ((CVal){.i = 1}),
        // After the first element.
        ((CVal){.i = 2}),
    }})},
    // Between the key and its value.
    {"gap", ((CVal){.i = 3})},
    // On the block scalar header.
    {"block", ((CVal){.s = "Text.\n"})},
    {"anchored", ((CVal){.i = 4})},
    {"alias", ((CVal){.i = 4})},
    // On the alias.
}});
    (void)my_data;
    return 0;
}
