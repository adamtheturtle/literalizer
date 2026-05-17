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
struct Record0 { const char *s; long long i; double f; bool b; const void *n; const char *d; const char *dt; const char *by; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .s = "string",
    .i = 1,
    .f = 1.5,
    .b = true,
    .n = NULL,
    .d = "2024-01-15",
    .dt = "2024-01-15T12:00:00",
    .by = "48656c6c6f",
};
    (void)my_data;
    return 0;
}
