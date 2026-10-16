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
    // null heading
    // before null
    {"a", ((CVal){.s = NULL})},  // first null
    {"b", ((CVal){.s = NULL})},  // second null
}});
    (void)my_data;
    return 0;
}
