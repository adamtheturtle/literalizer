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
    const long long expected[] = {1, 1};
    assert(event_index < 2 && actual == expected[event_index]);
    ++event_index;
}
static CVal capture(CVal __proto__) {
    observe_event(1); observe_event(__proto__.i);
    return (CVal){.i = __proto__.i + 100};
}
static void verify_events(void) { assert(event_index == 2); }
int main(void) {
capture(((CVal){.i = 1}));
verify_events();
    return 0;
}
