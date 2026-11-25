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
    {"metrics", ((CVal){.m = (CKV[]){{"count", ((CVal){.i = 100})}, {"rate", ((CVal){.i = 50})}}})},
    {"flags", ((CVal){.m = (CKV[]){{"retries", ((CVal){.i = 3})}, {"timeout", ((CVal){.i = 30})}}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"metrics", ((CVal){.m = (CKV[]){{"count", ((CVal){.i = 100})}, {"rate", ((CVal){.i = 50})}}})},
    {"flags", ((CVal){.m = (CKV[]){{"retries", ((CVal){.i = 3})}, {"timeout", ((CVal){.i = 30})}}})},
}});
    (void)my_data;
    return 0;
}
