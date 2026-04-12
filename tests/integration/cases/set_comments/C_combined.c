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
struct CKV { const char *k; CVal v; };  // NOLINT(altera-struct-pack-align)
static void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.s = "apple"}),  // inline comment
    // before banana
    ((CVal){.s = "banana"}),
    // trailing
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.s = "apple"}),  // inline comment
    // before banana
    ((CVal){.s = "banana"}),
    // trailing
}});
    (void)my_data;
}
