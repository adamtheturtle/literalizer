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
    ((CVal){.a = (CVal[]){((CVal){.i = 2}), ((CVal){.s = "hello"})}}),  // trailing note
    // next element
    ((CVal){.a = (CVal[]){((CVal){.i = 3}), ((CVal){.s = "world"})}}),
}});
(void)my_data;
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.a = (CVal[]){((CVal){.i = 2}), ((CVal){.s = "hello"})}}),  // trailing note
    // next element
    ((CVal){.a = (CVal[]){((CVal){.i = 3}), ((CVal){.s = "world"})}}),
}});
    (void)my_data;
    return 0;
}
