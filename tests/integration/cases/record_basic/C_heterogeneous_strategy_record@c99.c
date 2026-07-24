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
struct Record0 { long long id; const char *label; bool enabled; const CVal *related_ids; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .id = 1,
    .label = "She said \"hello\", then waved",
    .enabled = false,
    .related_ids = (CVal[]){
        ((CVal){.i = 1}),
        ((CVal){.i = 2}),
        ((CVal){.i = 3}),
    },
};
    (void)my_data;
    return 0;
}
