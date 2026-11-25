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
static void app_client_go_stub_(CVal _a0, CVal _a1) { (void)_a0, (void)_a1; }
struct clientType_ { void (*go)(CVal, CVal); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .go = app_client_go_stub_ } };
int main(void) {
app.client.go(((CVal){.a = (CVal[]){((CVal){.i = 1})}}), ((CVal){.a = (CVal[]){((CVal){.s = "text"})}}));
    return 0;
}
