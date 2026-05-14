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
static void app_client_fetch_stub_(CVal _a0) { (void)_a0; }
struct clientType_ { void (*fetch)(CVal); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .fetch = app_client_fetch_stub_ } };
int main(void) {
app.client.fetch(((CVal){.s = "hello"}));
app.client.fetch(((CVal){.s = "world"}));
    return 0;
}
