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
CVal my_var = ((CVal){.m = (CKV[]){
    {"_", ((CVal){.s = "_"})},
}});
CVal item_var = ((CVal){.m = (CKV[]){
    {"_", ((CVal){.s = "_"})},
}});
CVal my_data = ((CVal){.m = (CKV[]){
    {"key", my_var},
    {"items", ((CVal){.a = (CVal[]){item_var, ((CVal){.m = (CKV[]){{"fallback", ((CVal){.s = "value"})}}})}})},
}});
    (void)my_data;
    return 0;
}
