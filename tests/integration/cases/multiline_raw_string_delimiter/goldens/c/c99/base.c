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
CVal my_data = ((CVal){.a = (CVal[]){
    ((CVal){.s = "custom base after empty collision: )\"\nvalue"}),
    ((CVal){.s = "custom suffix after base collision: )\" and )x0\"\nvalue"}),
    ((CVal){.s = "custom second suffix: )\" and )x0\" and )x00\"\nvalue"}),
    ((CVal){.s = "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"}),
}});
    (void)my_data;
    return 0;
}
