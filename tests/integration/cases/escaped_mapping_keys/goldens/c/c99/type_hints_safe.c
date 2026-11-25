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
    {"quote\"backslash\\", ((CVal){.i = 1})},
    {"line\nbreak", ((CVal){.i = 2})},
    {"$(literal)${text}", ((CVal){.i = 3})},
    {"RStr prefix", ((CVal){.i = 4})},
}});
    (void)my_data;
    return 0;
}
