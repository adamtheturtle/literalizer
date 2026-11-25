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
struct Record0 { const CVal *items; };
int main(void) {
struct Record0 record_data = (struct Record0){
    .items = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    },
};
struct Record0 my_data = record_data;
    (void)my_data;
    return 0;
}
