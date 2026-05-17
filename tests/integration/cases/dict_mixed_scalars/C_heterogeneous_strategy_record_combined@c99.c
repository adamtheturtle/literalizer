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
struct Record0 { long long a; const char *b; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .a = 1,
    .b = "x",
};
(void)my_data;
my_data = (struct Record0){
    .a = 1,
    .b = "x",
};
    (void)my_data;
    return 0;
}
