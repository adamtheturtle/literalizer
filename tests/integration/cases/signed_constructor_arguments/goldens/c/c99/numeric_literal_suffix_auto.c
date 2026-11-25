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
    ((CVal){.i = -42L}),
    ((CVal){.i = 0L}),
    ((CVal){.i = 42L}),
    ((CVal){.f = -1.25}),
    ((CVal){.f = 0.0}),
    ((CVal){.f = 1.25}),
}});
    (void)my_data;
    return 0;
}
