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
    ((CVal){.a = (CVal[]){((CVal){.s = "set_task"}), ((CVal){.s = "web"}), ((CVal){.s = "lint_web"})}}),
    ((CVal){.a = (CVal[]){((CVal){.s = "merge_pipelines"})}}),
}});
    (void)my_data;
    return 0;
}
