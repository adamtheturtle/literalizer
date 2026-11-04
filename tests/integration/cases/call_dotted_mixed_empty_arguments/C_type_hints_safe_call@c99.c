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
static CVal thing_go_stub_(CVal _a0, CVal _a1, CVal _a2) { (void)_a0, (void)_a1, (void)_a2; return (CVal){0}; }
struct thingType_ { CVal (*go)(CVal, CVal, CVal); };
static const struct thingType_ thing = { .go = thing_go_stub_ };
int main(void) {
thing.go(((CVal){.a = (CVal[]){}}), ((CVal){.a = (CVal[]){((CVal){.i = 1})}}), ((CVal){.a = (CVal[]){}}));
thing.go(((CVal){.a = (CVal[]){((CVal){.s = "text"})}}), ((CVal){.a = (CVal[]){((CVal){.i = 2})}}), ((CVal){.a = (CVal[]){}}));
thing.go(((CVal){.a = (CVal[]){}}), ((CVal){.a = (CVal[]){((CVal){.s = "text"})}}), ((CVal){.a = (CVal[]){}}));
thing.go(((CVal){.a = (CVal[]){((CVal){.s = "text"})}}), ((CVal){.a = (CVal[]){((CVal){.i = 2})}}), ((CVal){.a = (CVal[]){((CVal){.i = 3})}}));
    return 0;
}
