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
struct Record1 { const CVal *numbers; const CVal *strings; };
struct Record0 { CVal omap_value; struct Record1 sibling_lists; const CVal *ref_marker_present; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .omap_value = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.i = 1})},
    }}),
    .sibling_lists = (struct Record1){
        .numbers = (CVal[]){
            ((CVal){.i = 1}),
            ((CVal){.i = 2}),
        },
        .strings = (CVal[]){
            ((CVal){.s = "x"}),
            ((CVal){.s = "y"}),
        },
    },
    .ref_marker_present = (CVal[]){
        ((CVal){.s = "$keep"}),
        ((CVal){.s = "z"}),
    },
};
    (void)my_data;
    return 0;
}
