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
static CVal outer_thing_go_stub_(void) { return (CVal){0}; }
struct thingType_ { CVal (*go)(void); };
struct outerType_ { struct thingType_ thing; };
static const struct outerType_ outer = { .thing = { .go = outer_thing_go_stub_ } };
int main(void) {
outer.thing.go();
    return 0;
}
