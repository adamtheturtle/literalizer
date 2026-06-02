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
int main(void) {
CVal my_data = ((CVal){.m = (CKV[]){
    {"user_name", ((CVal){.i = 1})},
    {"user.name", ((CVal){.i = 2})},
    {"user-name", ((CVal){.i = 3})},
    {"field_name_that_is_really_quite_long_one", ((CVal){.i = 4})},
    {"field_name_that_is_really_quite_long_two", ((CVal){.i = 5})},
}});
(void)my_data;
my_data = ((CVal){.m = (CKV[]){
    {"user_name", ((CVal){.i = 1})},
    {"user.name", ((CVal){.i = 2})},
    {"user-name", ((CVal){.i = 3})},
    {"field_name_that_is_really_quite_long_one", ((CVal){.i = 4})},
    {"field_name_that_is_really_quite_long_two", ((CVal){.i = 5})},
}});
    (void)my_data;
    return 0;
}
