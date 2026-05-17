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
struct Record1 { const char *name; long long age; };
struct Record0 { long long id; struct Record1 owner; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .id = 1,
    .owner = (struct Record1){
        .name = "Alice",
        .age = 30,
    },
};
    (void)my_data;
    return 0;
}
