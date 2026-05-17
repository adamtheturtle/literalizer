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
struct Record0 { long long id; const char *description; bool is_done; const CVal *blocks; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .id = 1,
    .description = "She said \"hello\", then waved",
    .is_done = false,
    .blocks = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
        ((CVal){.i = 3}),
    },
};
    (void)my_data;
    return 0;
}
