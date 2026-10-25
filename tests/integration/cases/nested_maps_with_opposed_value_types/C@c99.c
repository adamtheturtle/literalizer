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
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"input", ((CVal){.m = (CKV[]){{"name", ((CVal){.s = "alice"})}, {"city", ((CVal){.s = "paris"})}}})}, {"expected", ((CVal){.m = (CKV[]){{"count", ((CVal){.i = 1})}, {"total", ((CVal){.i = 2})}}})}}}),
    ((CVal){.m = (CKV[]){{"input", ((CVal){.m = (CKV[]){{"name", ((CVal){.i = 10})}, {"city", ((CVal){.i = 20})}}})}, {"expected", ((CVal){.m = (CKV[]){{"count", ((CVal){.s = "done"})}, {"total", ((CVal){.s = "pending"})}}})}}}),
}});
    (void)my_data;
    return 0;
}
