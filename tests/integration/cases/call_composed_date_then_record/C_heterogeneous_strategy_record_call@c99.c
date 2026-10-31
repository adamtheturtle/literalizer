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
struct Record0 { long long a; };
static void consume(CVal _a0, struct Record0 _a1) { (void)_a0, (void)_a1; }
int main(void) {
CVal stamp = ((CVal){.s = "2001-02-03"});
struct Record0 item = (struct Record0){
    .a = 1,
};
consume(stamp, item);
    return 0;
}
