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
static void process(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; }
int main(void) {
CVal my_ints = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
    ((CVal){.i = 3}),
}});
CVal my_strings = ((CVal){.a = (CVal[]){
    ((CVal){.s = "a"}),
    ((CVal){.s = "b"}),
}});
process(my_ints, ((CVal){.i = 42}));
process(my_strings, ((CVal){.i = 7}));
    return 0;
}
