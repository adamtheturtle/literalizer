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
int main(void) {
CVal my_data = ((CVal){.m = (CKV[]){
    {"date", ((CVal){.s = "0099-05-27"})},
    {"naive", ((CVal){.s = "0001-01-01T12:30:00"})},
    {"recent", ((CVal){.s = "2024-05-27T10:00:00"})},
}});
    (void)my_data;
    return 0;
}
