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
    ((CVal){.s = "1970-01-01T00:00:00.000001+00:00"}),
    ((CVal){.s = "1969-12-31T23:59:59.500000+00:00"}),
    ((CVal){.s = "1970-01-01T00:00:01+00:00"}),
}});
    (void)my_data;
    return 0;
}
