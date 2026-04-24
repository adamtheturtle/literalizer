#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool bl;
        long long integer;
        unsigned long long uinteger;
        double fp;
        const char *str;
        const CVal *arr;
        const CKV *dict;
    };
};
struct CKV { const char *key; CVal val; };
void check_(void) {
CVal my_data = ((CVal){.arr = (CVal[]){
    ((CVal){.integer = 1}),
    ((CVal){.str = "hello"}),
    ((CVal){.bl = true}),
    ((CVal){.str = NULL}),
}});
    (void)my_data;
}
