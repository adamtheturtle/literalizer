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
struct Record0 { long long a; const char *b; };
static void consume_widget(struct Record0 _a0) { (void)_a0; }
int main(void) {
consume_widget((struct Record0){
    .a = 1,
    .b = "x",
});
    return 0;
}
