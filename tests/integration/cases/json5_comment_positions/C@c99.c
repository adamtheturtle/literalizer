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
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    {"counts", ((CVal){.a = (CVal[]){
        // before the first item
        ((CVal){.i = 1}),  // inline block after the comma
        // before the second item
        ((CVal){.i = 2}),
        // trailing inside the array
    }})},  // after the nested collection
    {"more", ((CVal){.a = (CVal[]){
        ((CVal){.i = 3}),
        //
        // block heading
        // block continuation
        ((CVal){.i = 4}),  // final inline
    }})},
    // trailing inside the object
    // after the root
    // after the document
}});
    (void)my_data;
    return 0;
}
