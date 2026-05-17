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
struct Record1 { long long id; const char *label; };
struct Record0 { const char *name; struct Record1 items[2]; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .name = "box",
    .items = {
        (struct Record1){
            .id = 1,
            .label = "first",
        },
        (struct Record1){
            .id = 2,
            .label = "second",
        },
    },
};
    (void)my_data;
    return 0;
}
