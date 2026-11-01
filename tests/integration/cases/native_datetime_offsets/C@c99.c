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
    {"stamps", ((CVal){.a = (CVal[]){((CVal){.s = "2001-02-03T04:05:06+00:00:01"}), ((CVal){.s = "2001-02-03T04:05:06-00:00:01"}), ((CVal){.s = "2001-02-03T04:05:06+00:00:00.000001"}), ((CVal){.s = "2001-02-03T04:05:06-00:00:00.000001"}), ((CVal){.s = "2001-02-03T04:05:06+05:30:15.000001"}), ((CVal){.s = "2001-02-03T04:05:06-05:30:15.000001"})}})},
}});
    (void)my_data;
    return 0;
}
