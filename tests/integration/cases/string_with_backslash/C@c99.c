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
    ((CVal){.s = "C:\\path\\to\\file"}),
    ((CVal){.s = "back\\\\slash"}),
    ((CVal){.s = "hello \\\"world\\\""}),
    ((CVal){.s = "path\\to \"# file"}),
    ((CVal){.s = "trailing\\"}),
    ((CVal){.s = "both \"quotes''' here"}),
    ((CVal){.s = "line1\\nline2\nwith newline"}),
}});
    (void)my_data;
    return 0;
}
