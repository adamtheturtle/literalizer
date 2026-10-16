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
// scalar inline
// inline continuation
// scalar trailing
CVal my_data = ((CVal){.i = // scalar heading
// second heading line
42});
(void)my_data;
// scalar inline
// inline continuation
// scalar trailing
my_data = ((CVal){.i = // scalar heading
// second heading line
42});
    (void)my_data;
    return 0;
}
