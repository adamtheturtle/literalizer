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
#include <math.h>
int main(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.f = INFINITY}),
    ((CVal){.f = -INFINITY}),
    ((CVal){.f = NAN}),
}});
    (void)my_data;
    return 0;
}
