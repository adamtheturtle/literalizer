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
    {"a_b", ((CVal){.i = 0x1})},
    {"a-b", ((CVal){.i = 0x2})},
    {"averyveryverylongkeynamethatgoesonandonandon", ((CVal){.i = 0x3})},
    {"averyveryverylongkeynamethatgoesonandmore", ((CVal){.i = 0x4})},
}});
    (void)my_data;
    return 0;
}
