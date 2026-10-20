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
CVal actual = ((CVal){.i = 42});
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"$ref", ((CVal){.i = 1})}}}),
    ((CVal){.m = (CKV[]){{"$ref", ((CVal){.s = NULL})}}}),
    actual,
}});
    (void)my_data;
    return 0;
}
