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
struct Record0 { long long id; const char *label; const CVal *tags; };
int main(void) {
struct Record0 my_data[] = {
    (struct Record0){.id = 1, .label = "first", .tags = (CVal[]){}},
    (struct Record0){.id = 2, .label = "second", .tags = (CVal[]){}},
    (struct Record0){.id = 3, .label = "third", .tags = (CVal[]){}},
};
    (void)my_data;
    return 0;
}
