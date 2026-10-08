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
struct Record1 { long long integer; bool boolean; double decimal; const void *null; };
struct Record3 { long long integer; };
struct Record2 { struct Record3 child; };
struct Record4 { const char *text; };
struct Record5 { const char *day; const char *stamp; };
struct Record0 { struct Record1 trivial; struct Record2 nested; struct Record4 owning; struct Record5 calendar; };
int main(void) {
struct Record1 trivial = (struct Record1){
    .integer = 1,
    .boolean = true,
    .decimal = 1.5,
    .null = NULL,
};
struct Record2 nested = (struct Record2){
    .child = (struct Record3){
        .integer = 2,
    },
};
struct Record4 owning = (struct Record4){
    .text = "owned",
};
struct Record5 calendar = (struct Record5){
    .day = "2001-01-02",
    .stamp = "2001-01-02T03:04:05+00:00",
};
struct Record0 my_data = (struct Record0){
    .trivial = trivial,
    .nested = nested,
    .owning = owning,
    .calendar = calendar,
};
    (void)my_data;
    return 0;
}
