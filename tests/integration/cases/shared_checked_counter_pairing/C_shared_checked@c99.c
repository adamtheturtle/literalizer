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
#include <string.h>
static int calls = 0, checks = 0;
static bool accept(CVal user, CVal timestamp) {
    assert(strcmp(user.s, calls == 0 ? "user_1" : "user_2") == 0);
    assert(timestamp.f == 100.0 + calls);
    calls++;
    return strcmp(user.s, "user_1") == 0;
}
static void checkResult(bool actual, CVal expected) {
    assert(actual == expected.a[0].b);
    assert(strcmp(expected.a[1].s, checks == 0 ? "first" : "second") == 0);
    checks++;
}
int main(void) {
    const struct { bool (*accept)(CVal, CVal); } counter = {accept};
    checkResult(counter.accept(((CVal){.s = "user_1"}), ((CVal){.f = 100.0})), ((CVal){.a = (CVal[]){((CVal){.b = true}), ((CVal){.s = "first"})}}));
    checkResult(counter.accept(((CVal){.s = "user_2"}), ((CVal){.f = 101.0})), ((CVal){.a = (CVal[]){((CVal){.b = false}), ((CVal){.s = "second"})}}));
    assert(calls == 2 && checks == 2);
    return 0;
}
