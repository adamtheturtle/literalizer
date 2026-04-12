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
CVal my_data = ((CVal){.m = (CKV[]){
    {"users", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Bob"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "admin"}), ((CVal){.s = "user"})}})}}}), ((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Carol"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "guest"})}})}}})}})},
}});
my_data = ((CVal){.m = (CKV[]){
    {"users", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Bob"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "admin"}), ((CVal){.s = "user"})}})}}}), ((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Carol"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "guest"})}})}}})}})},
}});
    (void)my_data;
}
