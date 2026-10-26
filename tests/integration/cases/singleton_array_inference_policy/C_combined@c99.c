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
    {"below", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.i = 1})}})}})}})}})}})}})}})}})},
    {"boundary", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.i = 2})}})}})}})}})}})}})}})}})}})},
    {"multiple", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.i = 3})}})}})}})}})}})}})}})}})}})}})}})}})}})}})}})}})}})},
    {"text", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.s = "value"})}})}})}})}})}})}})}})}})}})},
    {"boolean", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.b = true})}})}})}})}})}})}})}})}})}})},
    {"float", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.f = 1.5})}})}})}})}})}})}})}})}})}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"below", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.i = 1})}})}})}})}})}})}})}})}})},
    {"boundary", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.i = 2})}})}})}})}})}})}})}})}})}})},
    {"multiple", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.i = 3})}})}})}})}})}})}})}})}})}})}})}})}})}})}})}})}})}})},
    {"text", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.s = "value"})}})}})}})}})}})}})}})}})}})},
    {"boolean", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.b = true})}})}})}})}})}})}})}})}})}})},
    {"float", ((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.a = (CVal[]){((CVal){.f = 1.5})}})}})}})}})}})}})}})}})}})},
}});
    (void)my_data;
    return 0;
}
