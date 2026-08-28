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
    // About the first dotted key.
    // About the second dotted key.
    {"dotted", ((CVal){.m = (CKV[]){{"first", ((CVal){.i = 1})}, {"second", ((CVal){.i = 2})}}})},
    {"plain", ((CVal){.i = 3})},  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    {"entries", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "one"})}}}), ((CVal){.m = (CKV[]){{"name", ((CVal){.s = "two"})}}})}})},
    // Inside the table.
    {"table", ((CVal){.m = (CKV[]){{"inner", ((CVal){.i = 4})}}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    // About the first dotted key.
    // About the second dotted key.
    {"dotted", ((CVal){.m = (CKV[]){{"first", ((CVal){.i = 1})}, {"second", ((CVal){.i = 2})}}})},
    {"plain", ((CVal){.i = 3})},  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    {"entries", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "one"})}}}), ((CVal){.m = (CKV[]){{"name", ((CVal){.s = "two"})}}})}})},
    // Inside the table.
    {"table", ((CVal){.m = (CKV[]){{"inner", ((CVal){.i = 4})}}})},
}});
    (void)my_data;
    return 0;
}
