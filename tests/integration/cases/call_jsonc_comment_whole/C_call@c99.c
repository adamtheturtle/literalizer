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
#include <assert.h>
static int event_index = 0;
static void observe_event(long long actual) {
    const long long expected[] = {1, 42};
    assert(event_index < 2 && actual == expected[event_index]);
    ++event_index;
}
static CVal f(CVal a) {
    observe_event(1); observe_event(a.i);
    return (CVal){.i = a.i + 100};
}
static void verify_events(void) { assert(event_index == 2); }
int main(void) {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(((CVal){.i = 42}));
verify_events();
    return 0;
}
