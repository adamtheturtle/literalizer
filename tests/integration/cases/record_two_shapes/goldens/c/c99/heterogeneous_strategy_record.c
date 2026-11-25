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
struct Record1 { long long count; long long rate; };
struct Record2 { long long retries; long long timeout; };
struct Record0 { struct Record1 metrics; struct Record2 flags; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .metrics = (struct Record1){
        .count = 100,
        .rate = 50,
    },
    .flags = (struct Record2){
        .retries = 3,
        .timeout = 30,
    },
};
    (void)my_data;
    return 0;
}
