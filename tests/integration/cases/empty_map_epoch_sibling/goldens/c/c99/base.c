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
    ((CVal){.m = (CKV[]){{"timestamp", ((CVal){.s = "2020-01-01T00:00:00+00:00"})}}}),
    ((CVal){.m = (CKV[]){}}),
}});
    (void)my_data;
    return 0;
}
