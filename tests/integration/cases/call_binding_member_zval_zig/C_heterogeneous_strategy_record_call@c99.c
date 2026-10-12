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
static CVal obj_ZVal_stub_(CVal _a0) { (void)_a0; return (CVal){0}; }
struct objType_ { CVal (*ZVal)(CVal); };
static const struct objType_ obj = { .ZVal = obj_ZVal_stub_ };
int main(void) {
CVal my_data = obj.ZVal(((CVal){.i = 42})); // note
    (void)my_data;
    return 0;
}
