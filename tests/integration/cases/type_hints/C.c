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
    {"name", ((CVal){.s = "Alice"})},
    {"age", ((CVal){.i = 30})},
    {"active", ((CVal){.b = true})},
    {"score", ((CVal){.s = NULL})},
    {"joined", ((CVal){.s = "2024-01-15"})},
    {"last_login", ((CVal){.s = "2024-01-15T12:30:00+00:00"})},
    {"avatar", ((CVal){.s = "48656c6c6f"})},
}});
    (void)my_data;
    return 0;
}
