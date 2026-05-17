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
struct Record0 { const char *name; const CVal *scores; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .name = "Alice",
    .scores = (CVal[]){
        ((CVal){.i = 10}),
        ((CVal){.i = 20}),
        ((CVal){.i = 30}),
    },
};
    (void)my_data;
    return 0;
}
