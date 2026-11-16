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
static int *event_index(void) { static int index = 0; return &index; }
static void observe_event(long long actual) {
    const long long expected[] = {1, 1, 2, 101, 3, 42};
    assert(*event_index() < 6 && actual == expected[*event_index()]);
    ++*event_index();
}
static CVal process(CVal argument) {
    observe_event(1); observe_event(argument.i);
    return (CVal){.i = argument.i + 100};
}
static void emit(CVal actual, CVal zipped) { observe_event(2); observe_event(actual.i); observe_event(3); observe_event(zipped.i); }
static void verify_events(void) { assert(*event_index() == 6); }
int main(void) {
emit(process(((CVal){.i = 1})), ((CVal){.i = 42}));
verify_events();
    return 0;
}
