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
    // strings stay data
    ((CVal){.s = "https://example.org/a/*b*/"}),  // URL annotation
    ((CVal){.s = "escaped quote: \" // still data"}),
    ((CVal){.s = "backslash: \\"}),  // outside the string
    ((CVal){.s = "/* not a comment */"}),
}});
(void)my_data;
my_data = ((CVal){.a = (CVal[]){
    // strings stay data
    ((CVal){.s = "https://example.org/a/*b*/"}),  // URL annotation
    ((CVal){.s = "escaped quote: \" // still data"}),
    ((CVal){.s = "backslash: \\"}),  // outside the string
    ((CVal){.s = "/* not a comment */"}),
}});
    (void)my_data;
    return 0;
}
