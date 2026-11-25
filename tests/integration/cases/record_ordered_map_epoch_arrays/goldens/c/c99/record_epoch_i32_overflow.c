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
struct Record0 { CVal values; bool flag; const CVal *direct_arrays; };
int main(void) {
struct Record0 my_data = (struct Record0){
    .values = ((CVal){.m = (CKV[]){
        {"wide", ((CVal){.a = (CVal[]){
            ((CVal){.a = (CVal[]){
                ((CVal){.i = 2208988800}),
            }}),
            ((CVal){.a = (CVal[]){}}),
        }})},
        {"narrow", ((CVal){.a = (CVal[]){
            ((CVal){.a = (CVal[]){
                ((CVal){.i = 946684800}),
            }}),
        }})},
        {"negative", ((CVal){.a = (CVal[]){
            ((CVal){.a = (CVal[]){
                ((CVal){.i = -2208988800}),
            }}),
        }})},
        {"shifted", ((CVal){.a = (CVal[]){
            ((CVal){.a = (CVal[]){
                ((CVal){.i = 2208988800}),
            }}),
        }})},
        {"mixed_width", ((CVal){.a = (CVal[]){
            ((CVal){.a = (CVal[]){
                ((CVal){.i = 946684800}),
            }}),
            ((CVal){.a = (CVal[]){
                ((CVal){.i = 2208988800}),
            }}),
        }})},
        {"text", ((CVal){.s = "preserve"})},
    }}),
    .flag = true,
    .direct_arrays = (CVal[]){
        ((CVal){.a = (CVal[]){
            ((CVal){.i = 2208988800}),
        }}),
        ((CVal){.a = (CVal[]){}}),
    },
};
    (void)my_data;
    return 0;
}
