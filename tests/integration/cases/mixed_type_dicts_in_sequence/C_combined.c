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
static void check_(void) {
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_1"})}, {"draft", ((CVal){.b = true})}}}),
    ((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_2"})}}}),
}});
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_1"})}, {"draft", ((CVal){.b = true})}}}),
    ((CVal){.m = (CKV[]){{"type", ((CVal){.s = "create"})}, {"pr_id", ((CVal){.s = "pr_2"})}}}),
}});
    (void)my_data;
}
