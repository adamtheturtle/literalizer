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
    ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 100})}, {"description", ((CVal){.s = "first task"})}, {"is_done", ((CVal){.b = false})}, {"blocks", ((CVal){.a = (CVal[]){((CVal){.i = 102}), ((CVal){.i = 103})}})}}}),
    ((CVal){.m = (CKV[]){{"id", ((CVal){.i = 101})}, {"description", ((CVal){.s = "second task"})}, {"is_done", ((CVal){.b = true})}, {"blocks", ((CVal){.a = (CVal[]){((CVal){.i = 100})}})}}}),
}});
    (void)my_data;
    return 0;
}
