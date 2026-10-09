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
struct Record1 { long long x; };
struct Record2 { const char *day; const char *stamp; };
struct Record0 { struct Record1 plain; struct Record2 timed; };
int main(void) {
struct Record1 plain = (struct Record1){
    .x = 1,
};
struct Record2 timed = (struct Record2){
    .day = "2001-01-02",
    .stamp = "2001-01-02T03:04:05+00:00",
};
struct Record0 my_data = (struct Record0){
    .plain = plain,
    .timed = timed,
};
    (void)my_data;
    return 0;
}
