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
struct Record1 { long long status; };
struct Record2 { const char *status; };
struct Record4 { const char *kind; bool urgent; };
struct Record3 { struct Record4 inner; };
struct Record6 { const char *error; };
struct Record5 { struct Record6 inner; };
struct Record7 { struct Record1 holder; };
struct Record8 { struct Record2 holder; };
struct Record9 { const CVal *nums; };
struct Record0 { struct Record1 plain; struct Record2 other; struct Record3 nested_a; struct Record5 nested_b; struct Record7 wrap_a; struct Record8 wrap_b; struct Record9 wide; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .plain = (struct Record1){
        .status = 1,
    },
    .other = (struct Record2){
        .status = "ready",
    },
    .nested_a = (struct Record3){
        .inner = (struct Record4){
            .kind = "add",
            .urgent = true,
        },
    },
    .nested_b = (struct Record5){
        .inner = (struct Record6){
            .error = "not_found",
        },
    },
    .wrap_a = (struct Record7){
        .holder = (struct Record1){
            .status = 2,
        },
    },
    .wrap_b = (struct Record8){
        .holder = (struct Record2){
            .status = "word",
        },
    },
    .wide = (struct Record9){
        .nums = (CVal[]){
            ((CVal){.i = 1}),
            ((CVal){.i = 1099511627776}),
        },
    },
};
    (void)my_data;
    return 0;
}
