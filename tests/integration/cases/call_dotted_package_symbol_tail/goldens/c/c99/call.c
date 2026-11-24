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
static void helper_list_stub_(CVal _a0) { (void)_a0; }
struct helperType_ { void (*list)(CVal); };
static const struct helperType_ helper = { .list = helper_list_stub_ };
int main(void) {
helper.list(((CVal){.i = 1}));
    return 0;
}
