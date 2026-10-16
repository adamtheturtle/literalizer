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
    {"lower", ((CVal){.i = 3735928559})},
    {"upper", ((CVal){.i = 31})},
    {"negative", ((CVal){.i = -16})},
    {"zero", ((CVal){.i = 0})},
}});
    (void)my_data;
    return 0;
}
