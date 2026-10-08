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
struct Record0 { const char *value; };
static void consume(CVal _a0) { (void)_a0; }
int main(void) {
struct Record0 item = (struct Record0){
    .value = "owned",
};
consume(item);
    return 0;
}
