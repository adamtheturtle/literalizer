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
struct Record0 { const char *name; CVal payload; };
int main(void) {
struct Record0 my_data[] = {
    (struct Record0){
        .name = "one",
        .payload = ((CVal){.m = (CKV[]){
            {"scalar", ((CVal){.i = 1})},
            {"items", ((CVal){.a = (CVal[]){
                ((CVal){.i = 2}),
                ((CVal){.i = 3}),
            }})},
        }}),
    },
    (struct Record0){
        .name = "two",
        .payload = ((CVal){.m = (CKV[]){
            {"other", ((CVal){.i = 2})},
        }}),
    },
};
    (void)my_data;
    return 0;
}
