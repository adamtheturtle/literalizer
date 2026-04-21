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
static void app_client_fetch_stub_() {}
struct clientType_ { void (*fetch)(); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .fetch = app_client_fetch_stub_ } };
void check_(void) {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(((CVal){.b = true}));
}
