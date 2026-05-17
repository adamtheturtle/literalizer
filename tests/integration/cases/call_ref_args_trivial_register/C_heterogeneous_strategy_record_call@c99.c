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
static void process(CVal _a0, CVal _a1) { (void)_a0; (void)_a1; }
int main(void) {
CVal my_int = ((CVal){.i = 1});
CVal my_bool = ((CVal){.b = true});
CVal my_float = ((CVal){.f = 3.14});
CVal my_list = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
    ((CVal){.i = 3}),
}});
process(my_int, ((CVal){.i = 42}));
process(my_bool, ((CVal){.i = 7}));
process(my_float, ((CVal){.i = 9}));
process(my_list, ((CVal){.i = 1}));
    return 0;
}
