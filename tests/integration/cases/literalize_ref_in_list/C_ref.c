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
CVal val_x = ((CVal){.m = (CKV[]){
    {"_", ((CVal){.s = "_"})},
}});
CVal val_y = ((CVal){.m = (CKV[]){
    {"_", ((CVal){.s = "_"})},
}});
CVal my_data = ((CVal){.a = (CVal[]){
    val_x,
    val_y,
}});
    (void)my_data;
    return 0;
}
