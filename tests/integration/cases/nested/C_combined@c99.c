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
    {"users", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Bob"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "admin"}), ((CVal){.s = "user"})}})}}}), ((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Carol"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "guest"})}})}}})}})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"users", ((CVal){.a = (CVal[]){((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Bob"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "admin"}), ((CVal){.s = "user"})}})}}}), ((CVal){.m = (CKV[]){{"name", ((CVal){.s = "Carol"})}, {"tags", ((CVal){.a = (CVal[]){((CVal){.s = "guest"})}})}}})}})},
}});
    (void)my_data;
    return 0;
}
