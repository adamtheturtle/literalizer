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
struct Record0 { long long a; long long b; const char *c; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .a = 1,
    .b = 3000000000,
    .c = "x",
};
    (void)my_data;
    return 0;
}
