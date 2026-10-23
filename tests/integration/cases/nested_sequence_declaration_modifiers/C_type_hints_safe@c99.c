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
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.a = (CVal[]){}}),
    ((CVal){.a = (CVal[]){((CVal){.i = 1})}}),
    ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.i = 2})}}),
    ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.s = "x"}), ((CVal){.b = true}), ((CVal){.s = NULL})}}),
    ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.i = 2}), ((CVal){.i = 3}), ((CVal){.i = 4}), ((CVal){.i = 5}), ((CVal){.i = 6}), ((CVal){.i = 7}), ((CVal){.i = 8})}}),
}});
    (void)my_data;
    return 0;
}
