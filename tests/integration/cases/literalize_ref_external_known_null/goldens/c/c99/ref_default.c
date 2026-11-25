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
CVal item = ((CVal){.s = NULL});
CVal my_data = ((CVal){.s = NULL});
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
    return 0;
}
