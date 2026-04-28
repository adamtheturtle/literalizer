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
int main(void) {
CVal my_data = ((CVal){.dict = (CKV[]){
    {"name", ((CVal){.str = "Alice"})},
    {"age", ((CVal){.integer = 30})},
    {"active", ((CVal){.bl = true})},
    {"score", ((CVal){.str = NULL})},
}});
    (void)my_data;
    return 0;
}
