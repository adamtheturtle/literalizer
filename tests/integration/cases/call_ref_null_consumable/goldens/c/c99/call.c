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
static void consume(CVal _a0) { (void)_a0; }
int main(void) {
CVal my_null = ((CVal){.s = NULL});
CVal regular_null = ((CVal){.s = NULL});
consume(my_null);
consume(regular_null);
    return 0;
}
