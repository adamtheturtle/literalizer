#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.b = true}),
    ((CVal){.i = 42}),
    ((CVal){.s = "apple"}),
}});
    (void)my_data;
}
