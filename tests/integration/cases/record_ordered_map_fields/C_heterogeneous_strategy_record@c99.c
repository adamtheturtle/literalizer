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
struct Record0 { CVal numbers; CVal words; CVal nested; CVal empty; bool flag; CVal nested_maps; CVal empty_nested_maps; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .numbers = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.i = 1})},
    }}),
    .words = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.s = "s"})},
    }}),
    .nested = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.a = (CVal[]){
            ((CVal){.i = 1}),
            ((CVal){.i = 2}),
        }})},
    }}),
    .empty = ((CVal){.m = (CKV[]){}}),
    .flag = true,
    .nested_maps = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.m = (CKV[]){
            {"nested", ((CVal){.i = 1})},
        }})},
    }}),
    .empty_nested_maps = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.m = (CKV[]){}})},
    }}),
};
    (void)my_data;
    return 0;
}
