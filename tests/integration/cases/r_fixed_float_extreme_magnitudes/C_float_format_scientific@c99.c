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
    ((CVal){.f = 5.0e-324}),
    ((CVal){.f = 2.2250738585072014e-308}),
    ((CVal){.f = 1.0e-307}),
    ((CVal){.f = 1.0e21}),
    ((CVal){.f = -1.5e300}),
    ((CVal){.f = 1.7976931348623157e308}),
    ((CVal){.f = -1.7976931348623157e308}),
}});
    (void)my_data;
    return 0;
}
