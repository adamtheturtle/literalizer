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
static int *callCount(void) { static int count = 0; return &count; }
static int *checkCount(void) { static int count = 0; return &count; }
static bool accept(CVal user, CVal timestamp) {
    assert(strcmp(user.s, *callCount() == 0 ? "user_1" : "user_2") == 0);
    assert(timestamp.f == 100.0 + *callCount());
    (*callCount())++;
    return strcmp(user.s, "user_1") == 0;
}
static void checkResult(bool actual, CVal expected) {
    assert(actual == expected.a[0].b);
    assert(strcmp(expected.a[1].s, *checkCount() == 0 ? "first" : "second") == 0);
    (*checkCount())++;
}
int main(void) {
    const struct { bool (*accept)(CVal, CVal); } counter = {accept};
    checkResult(counter.accept(((CVal){.s = "user_1"}), ((CVal){.f = 100.0})), ((CVal){.a = (CVal[]){((CVal){.b = true}), ((CVal){.s = "first"})}}));
    assert(*callCount() == 1 && *checkCount() == 1);
    return 0;
}
