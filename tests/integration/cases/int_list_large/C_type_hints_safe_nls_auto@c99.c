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
    ((CVal){.i = 1000000L}),
    ((CVal){.i = -1234L}),
    ((CVal){.i = 255L}),
    ((CVal){.i = -10L}),
}});
    (void)my_data;
    return 0;
}
