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
static CVal thing_go_stub_(CVal _a0) { (void)_a0; return (CVal){0}; }
struct thingType_ { CVal (*go)(CVal); };
static const struct thingType_ thing = { .go = thing_go_stub_ };
int main(void) {
CVal item = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
}});
thing.go(item);
    return 0;
}
