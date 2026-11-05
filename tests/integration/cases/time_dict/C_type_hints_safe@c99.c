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
    {"morning", ((CVal){.s = "09:30:00"})},
    {"afternoon", ((CVal){.s = "14:15:00"})},
    {"evening", ((CVal){.s = "23:59:59"})},
}});
    (void)my_data;
    return 0;
}
