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
static void make_widget(CVal _a0, CVal _a1) { (void)_a0, (void)_a1; }
int main(void) {
make_widget(((CVal){.a = (CVal[]){((CVal){.i = 1})}}), ((CVal){.a = (CVal[]){((CVal){.i = 2})}}));
    return 0;
}
