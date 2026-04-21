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
static int app_client_fetch_stub_() { return 0; }
struct clientType_ { int (*fetch)(); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .fetch = app_client_fetch_stub_ } };
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
void emit();
void check_(void) {
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(((CVal){.b = true})));
}
