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
struct Record0 { const char *name; const CVal *values; };
static void consume(struct Record0 _a0) { (void)_a0; }
int main(void) {
struct Record0 item = (struct Record0){
    .name = "first",
    .values = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
    },
};
consume(item);
    return 0;
}
