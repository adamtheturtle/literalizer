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
static void my_app_http_client_fetch_stub_(CVal _a0) { (void)_a0; }
struct http_clientType_ { void (*fetch)(CVal); };
struct my_appType_ { struct http_clientType_ http_client; };
static const struct my_appType_ my_app = { .http_client = { .fetch = my_app_http_client_fetch_stub_ } };
void check_(void) {
my_app.http_client.fetch(((CVal){.s = "hello"}));
my_app.http_client.fetch(((CVal){.i = 42}));
my_app.http_client.fetch(((CVal){.b = true}));
}
