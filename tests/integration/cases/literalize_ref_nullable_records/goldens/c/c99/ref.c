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
struct Record1 { long long x; const void *y; };
struct Record2 { const void *x; const void *y; };
struct Record3 { long long x; long long y; };
struct Record0 { struct Record1 nullable; struct Record2 null_fields; struct Record3 plain; };
int main(void) {
struct Record1 nullable = (struct Record1){
    .x = 1,
    .y = NULL,
};
struct Record2 null_fields = (struct Record2){
    .x = NULL,
    .y = NULL,
};
struct Record3 plain = (struct Record3){
    .x = 1,
    .y = 2,
};
struct Record0 my_data = (struct Record0){
    .nullable = nullable,
    .null_fields = null_fields,
    .plain = plain,
};
    (void)my_data;
    return 0;
}
