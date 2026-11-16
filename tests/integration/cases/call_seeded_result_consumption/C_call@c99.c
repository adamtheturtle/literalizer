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
    const long long expected[] = {2, 0, 1, 1, 2, 101};
    assert(*event_index() < 6 && actual == expected[*event_index()]);
    ++*event_index();
}
static CVal make_widget(CVal argument) {
    observe_event(1); observe_event(argument.i);
    return (CVal){.i = argument.i + 100};
}
static void consume_widget(CVal argument) { observe_event(2); observe_event(argument.i); }
static void verify_events(void) { assert(*event_index() == 6); }
int main(void) {
CVal my_data = ((CVal){.i = 0});
consume_widget(my_data);
my_data = make_widget(((CVal){.i = 1}));
consume_widget(my_data);
verify_events();
    return 0;
}
