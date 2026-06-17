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
static CVal record_value(CVal _a0) { (void)_a0; return (CVal){0}; }
static void flush_buffer(CVal _a0) { (void)_a0; }
static void emit(CVal _a0) { (void)_a0; }
int main(void) {
emit(record_value(((CVal){.i = 42})));
flush_buffer(((CVal){.i = 3}));
    return 0;
}
