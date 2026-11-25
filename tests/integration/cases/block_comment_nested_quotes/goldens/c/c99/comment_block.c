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
CVal my_data = ((CVal){.m = (CKV[]){
    /* "{-" and '{-' stay readable */
    /* balanced {- nested -} and trailing -} stay readable */
    {"x", ((CVal){.i = 1})},
}});
    (void)my_data;
    return 0;
}
