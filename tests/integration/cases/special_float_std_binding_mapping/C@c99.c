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
#include <math.h>
int main(void) {
CVal std = ((CVal){.m = (CKV[]){
    {"nan", ((CVal){.f = NAN})},
    {"positive", ((CVal){.f = INFINITY})},
    {"negative", ((CVal){.f = -INFINITY})},
}});
    (void)std;
    return 0;
}
