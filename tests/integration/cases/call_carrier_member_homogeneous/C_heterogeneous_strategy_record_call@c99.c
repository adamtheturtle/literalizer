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
static void app_go_stub_(CVal _a0, CVal _a1) { (void)_a0, (void)_a1; }
struct appType_ { void (*go)(CVal, CVal); };
static const struct appType_ app = { .go = app_go_stub_ };
int main(void) {
app.go(((CVal){.a = (CVal[]){((CVal){.i = 1})}}), ((CVal){.a = (CVal[]){((CVal){.i = 2})}}));
    return 0;
}
