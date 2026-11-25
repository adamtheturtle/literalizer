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
    {"rows", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"replacement", ((CVal){.i = -1})}, {"present", ((CVal){.i = 1})}}}), ((CVal){.m = (CKV[]){{"replacement", ((CVal){.i = 2})}, {"present", ((CVal){.i = 3})}}})}})},
}});
    (void)my_data;
    return 0;
}
