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
int main(void) {
CVal my_data = ((CVal){.m = (CKV[]){
    {"within_i32", ((CVal){.s = "2024-01-15T12:00:00"})},
    {"beyond_i32", ((CVal){.s = "2099-06-15T08:30:00"})},
}});
    (void)my_data;
    return 0;
}
