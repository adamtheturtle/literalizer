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
    ((CVal){.i = 0}),
    ((CVal){.i = 1}),
    ((CVal){.i = -1}),
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.i = 0}),
    ((CVal){.i = 1}),
    ((CVal){.i = -1}),
}});
    (void)my_data;
}
