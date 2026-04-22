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
void process(CVal);
void check_(void) {
process(((CVal){.s = "hello"}));
process(((CVal){.i = 42}));
process(((CVal){.b = true}));
}
