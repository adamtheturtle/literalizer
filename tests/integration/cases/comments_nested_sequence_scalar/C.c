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
    ((CVal){.a = (CVal[]){((CVal){.s = "ADD"}), ((CVal){.s = "alice"}), ((CVal){.s = "hello"})}}),
    ((CVal){.a = (CVal[]){((CVal){.s = "DEL"}), ((CVal){.s = "bob"}), ((CVal){.s = "5"})}}),  // removes "world"
}});
    (void)my_data;
    return 0;
}
