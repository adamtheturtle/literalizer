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
static CVal make_widget(CVal _a0) { (void)_a0; return (CVal){0}; }
int main(void) {
CVal result = ((CVal){.i = make_widget(((CVal){.i = 42}))});
    (void)result;
    return 0;
}
