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
    ((CVal){.s = "1901-12-13T20:45:51"}),
    ((CVal){.s = "1901-12-13T20:45:52"}),
    ((CVal){.s = "2038-01-19T03:14:07"}),
    ((CVal){.s = "2038-01-19T03:14:08"}),
}});
    (void)my_data;
    return 0;
}
