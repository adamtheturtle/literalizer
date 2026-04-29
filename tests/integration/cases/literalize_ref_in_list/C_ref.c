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
CVal x = ((CVal){.i = 0});
CVal y = ((CVal){.i = 0});
CVal my_data = ((CVal){.a = (CVal[]){
    x,
    y,
}});
    (void)my_data;
    return 0;
}
