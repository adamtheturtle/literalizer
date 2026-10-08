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
    {"comma_hash", ((CVal){.s = "a,#b"})},
    {"comma_space_hash", ((CVal){.s = "trail, # comment"})},
    {"escaped_quote", ((CVal){.s = "quote \" and , #"})},
    {"next_line", ((CVal){.s = "xy"})},
    {"line_separator", ((CVal){.s = "x y"})},
    {"paragraph_separator", ((CVal){.s = "x y"})},
}});
    (void)my_data;
    return 0;
}
