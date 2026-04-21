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
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
int process();
void check_(void) {
process("hello");
process(42);
process(((CVal){.b = true}));
}
