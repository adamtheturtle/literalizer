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
static void process(CVal _a0, CVal _a1, CVal _a2, CVal _a3, CVal _a4, CVal _a5, CVal _a6, CVal _a7, CVal _a8, CVal _a9, CVal _a10, CVal _a11, CVal _a12, CVal _a13, CVal _a14, CVal _a15, CVal _a16, CVal _a17, CVal _a18, CVal _a19, CVal _a20, CVal _a21, CVal _a22, CVal _a23, CVal _a24, CVal _a25, CVal _a26) { (void)_a0; (void)_a1; (void)_a2; (void)_a3; (void)_a4; (void)_a5; (void)_a6; (void)_a7; (void)_a8; (void)_a9; (void)_a10; (void)_a11; (void)_a12; (void)_a13; (void)_a14; (void)_a15; (void)_a16; (void)_a17; (void)_a18; (void)_a19; (void)_a20; (void)_a21; (void)_a22; (void)_a23; (void)_a24; (void)_a25; (void)_a26; }
int main(void) {
process(((CVal){.i = 0}), ((CVal){.i = 1}), ((CVal){.i = 2}), ((CVal){.i = 3}), ((CVal){.i = 4}), ((CVal){.i = 5}), ((CVal){.i = 6}), ((CVal){.i = 7}), ((CVal){.i = 8}), ((CVal){.i = 9}), ((CVal){.i = 10}), ((CVal){.i = 11}), ((CVal){.i = 12}), ((CVal){.i = 13}), ((CVal){.i = 14}), ((CVal){.i = 15}), ((CVal){.i = 16}), ((CVal){.i = 17}), ((CVal){.i = 18}), ((CVal){.i = 19}), ((CVal){.i = 20}), ((CVal){.i = 21}), ((CVal){.i = 22}), ((CVal){.i = 23}), ((CVal){.i = 24}), ((CVal){.i = 25}), ((CVal){.i = 26}));
    return 0;
}
