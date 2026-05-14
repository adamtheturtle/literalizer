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
static void process(CVal _a0) { (void)_a0; }
int main(void) {
CVal my_var = ((CVal){.i = 42});
CVal my_other = ((CVal){.i = 7});
process(((CVal){.a = (CVal[]){my_var, ((CVal){.i = 42}), ((CVal){.s = "static"})}}));
process(((CVal){.a = (CVal[]){my_other, ((CVal){.i = 7}), ((CVal){.s = "label"})}}));
    return 0;
}
