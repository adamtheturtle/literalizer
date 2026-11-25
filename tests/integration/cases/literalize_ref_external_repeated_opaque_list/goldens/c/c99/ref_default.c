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
CVal item = ((CVal){.a = (CVal[]){}});
CVal my_data = ((CVal){.a = (CVal[]){
    item,
    item,
}});
consume_widget(my_data);
    return 0;
}
