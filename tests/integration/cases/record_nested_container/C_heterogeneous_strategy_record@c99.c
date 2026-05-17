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
struct Record0 { const char *title; const CVal *tags; long long priority; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .title = "report",
    .tags = (CVal[]){
        ((CVal){.s = "draft"}),
        ((CVal){.s = "urgent"}),
        ((CVal){.s = "review"}),
    },
    .priority = 2,
};
    (void)my_data;
    return 0;
}
