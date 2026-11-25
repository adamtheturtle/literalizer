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
static CVal make_widget(CVal _a0) { (void)_a0; return (CVal){0}; }
static void consume(CVal _a0) { (void)_a0; }
int main(void) {
CVal my_data = make_widget(((CVal){.s = NULL}));
consume(my_data);
my_data = make_widget(((CVal){.i = 42}));
consume(my_data);
    return 0;
}
