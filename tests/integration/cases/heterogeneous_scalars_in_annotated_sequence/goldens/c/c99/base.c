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
    ((CVal){.b = true}),
    ((CVal){.f = 1.5}),
    ((CVal){.s = NULL}),
    ((CVal){.s = "2020-01-01"}),
    ((CVal){.s = "2020-01-01T00:00:00+00:00"}),
    ((CVal){.a = (CVal[]){}}),
}});
    (void)my_data;
    return 0;
}
