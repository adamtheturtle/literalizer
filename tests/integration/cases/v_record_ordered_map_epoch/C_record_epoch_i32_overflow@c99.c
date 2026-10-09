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
struct Record0 { CVal values; bool flag; CVal nested_values; CVal list_values; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .values = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.i = 2208988800})},
    }}),
    .flag = true,
    .nested_values = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.m = (CKV[]){
            {"nested", ((CVal){.i = 2208988800})},
        }})},
    }}),
    .list_values = ((CVal){.m = (CKV[]){
        {"first", ((CVal){.a = (CVal[]){
            ((CVal){.i = 2208988800}),
        }})},
    }}),
};
    (void)my_data;
    return 0;
}
