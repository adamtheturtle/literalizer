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
struct Record0 { long long x; };
int main(void) {
struct Record0 first[] = {
    (struct Record0){.x = 1},
    (struct Record0){.x = 2},
};
const struct Record0 * my_data = first;
    (void)my_data;
    return 0;
}
