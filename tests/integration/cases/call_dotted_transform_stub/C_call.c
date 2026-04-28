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
static CVal process(CVal _a0) { (void)_a0; return (CVal){0}; }
static void log_emit_stub_(CVal _a0) { (void)_a0; }
struct logType_ { void (*emit)(CVal); };
static const struct logType_ log = { .emit = log_emit_stub_ };
int main(void) {
log.emit(process(((CVal){.s = "hello"})));
log.emit(process(((CVal){.i = 42})));
log.emit(process(((CVal){.b = true})));
    return 0;
}
