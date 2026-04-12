#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
void check_(void) {
CVal my_data = ((CVal){.s = "2024-01-15T00:00:00"});
my_data = ((CVal){.s = "2024-01-15T00:00:00"});
    (void)my_data;
}
