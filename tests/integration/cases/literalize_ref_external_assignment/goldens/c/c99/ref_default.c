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
static void consume_widget(CVal _a0) { (void)_a0; }
int main(void) {
CVal ref_data = ((CVal){.a = (CVal[]){
    ((CVal){.i = 1}),
    ((CVal){.i = 2}),
}});
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.i = 0}),
}});
consume_widget(my_data);
my_data = ref_data;
consume_widget(my_data);
    return 0;
}
