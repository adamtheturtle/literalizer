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
struct Record0 { const char *name; long long age; bool active; double score; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .name = "Alice",
    .age = 30,
    .active = true,
    .score = 4.5,
};
    (void)my_data;
    return 0;
}
