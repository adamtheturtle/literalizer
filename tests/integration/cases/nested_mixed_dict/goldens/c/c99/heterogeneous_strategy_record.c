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
struct Record1 { long long a; const char *b; const void *c; };
struct Record0 { struct Record1 outer; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .outer = (struct Record1){
        .a = 1,
        .b = "x",
        .c = NULL,
    },
};
    (void)my_data;
    return 0;
}
