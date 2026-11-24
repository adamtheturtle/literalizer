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
struct Record0 { const char *call; const CVal *args; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .call = "send",
    .args = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.s = "email"}),
        ((CVal){.s = "a@gmail.com"}),
        ((CVal){.i = 100}),
    },
};
    (void)my_data;
    return 0;
}
