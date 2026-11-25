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
    {"a", ((CVal){.m = (CKV[]){
        {"b", ((CVal){.a = (CVal[]){((CVal){.i = 1})}})},
        // Outdented from the sequence, so the inner mapping claims this.
        {"c", ((CVal){.i = 2})},
    }})},
    // Outdented from the inner mapping too, so the root claims this.
    {"d", ((CVal){.i = 3})},
}});
    (void)my_data;
    return 0;
}
