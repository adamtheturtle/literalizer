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
    ((CVal){.m = (CKV[]){{"call", ((CVal){.s = "send"})}, {"args", ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.s = "email"}), ((CVal){.s = "a@gmail.com"}), ((CVal){.i = 100})}})}}}),
    ((CVal){.m = (CKV[]){{"call", ((CVal){.s = "recv"})}, {"args", ((CVal){.a = (CVal[]){((CVal){.i = 2}), ((CVal){.s = "sms"}), ((CVal){.s = "b@example.com"}), ((CVal){.i = 200})}})}}}),
}});
(void)my_data;
my_data = ((CVal){.a = (CVal[]){
    ((CVal){.m = (CKV[]){{"call", ((CVal){.s = "send"})}, {"args", ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.s = "email"}), ((CVal){.s = "a@gmail.com"}), ((CVal){.i = 100})}})}}}),
    ((CVal){.m = (CKV[]){{"call", ((CVal){.s = "recv"})}, {"args", ((CVal){.a = (CVal[]){((CVal){.i = 2}), ((CVal){.s = "sms"}), ((CVal){.s = "b@example.com"}), ((CVal){.i = 200})}})}}}),
}});
    (void)my_data;
    return 0;
}
