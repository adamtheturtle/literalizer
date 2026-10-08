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
struct Record1 { long long value; };
struct Record0 { struct Record1 child; };
int main(void) {
struct Record0 first = (struct Record0){
    .child = (struct Record1){
        .value = 1,
    },
};
CVal my_data = first;
    (void)my_data;
    return 0;
}
