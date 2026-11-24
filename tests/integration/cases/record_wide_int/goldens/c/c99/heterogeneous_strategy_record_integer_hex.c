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
struct Record0 { long long quantity; unsigned long long big; double ratio; const char *label; bool ok; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .quantity = 0xf4240,
    .big = 18446744073709551615ULL,
    .ratio = 2.5,
    .label = "tag",
    .ok = true,
};
    (void)my_data;
    return 0;
}
