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
static CVal make_widget(CVal _a0, CVal _a1, CVal _a2) { (void)_a0, (void)_a1, (void)_a2; return (CVal){0}; }
int main(void) {
make_widget(((CVal){.a = (CVal[]){}}), ((CVal){.a = (CVal[]){((CVal){.i = 1})}}), ((CVal){.a = (CVal[]){}}));
make_widget(((CVal){.a = (CVal[]){((CVal){.s = "text"})}}), ((CVal){.a = (CVal[]){((CVal){.i = 2})}}), ((CVal){.a = (CVal[]){}}));
make_widget(((CVal){.a = (CVal[]){}}), ((CVal){.a = (CVal[]){((CVal){.s = "text"})}}), ((CVal){.a = (CVal[]){}}));
make_widget(((CVal){.a = (CVal[]){((CVal){.s = "text"})}}), ((CVal){.a = (CVal[]){((CVal){.i = 2})}}), ((CVal){.a = (CVal[]){((CVal){.i = 3})}}));
    return 0;
}
