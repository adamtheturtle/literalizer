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
    {"half", ((CVal){.s = "1979-05-27T07:32:00.500000"})},
    {"milli", ((CVal){.s = "1979-05-27T07:32:00.100000"})},
    {"max_milli", ((CVal){.s = "1979-05-27T07:32:00.999000"})},
    {"whole", ((CVal){.s = "1979-05-27T07:32:00"})},
}});
    (void)my_data;
    return 0;
}
