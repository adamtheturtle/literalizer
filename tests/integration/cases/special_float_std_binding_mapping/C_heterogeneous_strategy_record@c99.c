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
struct Record0 { double nan; double positive; double negative; };
int main(void) {
struct Record0 std = (struct Record0){
    .nan = NAN,
    .positive = INFINITY,
    .negative = -INFINITY,
};
    (void)std;
    return 0;
}
