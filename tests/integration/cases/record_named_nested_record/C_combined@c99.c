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
    {"collection", ((CVal){.s = "alpha"})},
    {"featured_entry", ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 100})}, {"label", ((CVal){.s = "first entry"})}, {"enabled", ((CVal){.b = false})}, {"related_ids", ((CVal){.a = (CVal[]){((CVal){.i = 102}), ((CVal){.i = 103})}})}}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"collection", ((CVal){.s = "alpha"})},
    {"featured_entry", ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 100})}, {"label", ((CVal){.s = "first entry"})}, {"enabled", ((CVal){.b = false})}, {"related_ids", ((CVal){.a = (CVal[]){((CVal){.i = 102}), ((CVal){.i = 103})}})}}})},
}});
    (void)my_data;
    return 0;
}
