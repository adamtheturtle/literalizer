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
struct Record0 { long long within_i32; long long beyond_i32; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .within_i32 = 1705320000,
    .beyond_i32 = 4085195400,
};
    (void)my_data;
    return 0;
}
