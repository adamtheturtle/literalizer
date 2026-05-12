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
    {"sibling_lists", ((CVal){.m = (CKV[]){{"numbers", ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.i = 2})}})}, {"strings", ((CVal){.a = (CVal[]){((CVal){.s = "x"}), ((CVal){.s = "y"})}})}}})},
    {"ref_marker_present", ((CVal){.a = (CVal[]){((CVal){.s = "$keep"}), ((CVal){.s = "z"})}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"sibling_lists", ((CVal){.m = (CKV[]){{"numbers", ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.i = 2})}})}, {"strings", ((CVal){.a = (CVal[]){((CVal){.s = "x"}), ((CVal){.s = "y"})}})}}})},
    {"ref_marker_present", ((CVal){.a = (CVal[]){((CVal){.s = "$keep"}), ((CVal){.s = "z"})}})},
}});
    (void)my_data;
    return 0;
}
