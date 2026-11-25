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
CVal array_value = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
}});
CVal scalar_value = ((CVal){.i = 3});
CVal my_data = ((CVal){.a = (CVal[]){
    array_value,
    scalar_value,
}});
    (void)my_data;
    return 0;
}
