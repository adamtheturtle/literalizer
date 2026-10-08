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
struct Record1 { const char *x; };
struct Record2 { long long x; };
struct Record0 { struct Record1 direct; struct Record2 bound; };
int main(void) {
struct Record0 first = (struct Record2){
    .x = 1,
};
struct Record0 my_data = (struct Record0){
    .direct = (struct Record1){
        .x = "s",
    },
    .bound = first,
};
    (void)my_data;
    return 0;
}
