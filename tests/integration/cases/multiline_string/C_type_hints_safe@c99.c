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
    ((CVal){.s = "first line\n  indented\n\nlast line"}),
    ((CVal){.s = "\nleading newline"}),
    ((CVal){.s = " \t\nleading whitespace"}),
    ((CVal){.s = "trailing newline\n"}),
    ((CVal){.s = "\nleading and trailing\n"}),
    ((CVal){.s = "quotes: \"\"\" ''' ` and backslash: \\"}),
    ((CVal){.s = "interpolation: ${value} #{value} #@value #$value $value"}),
    ((CVal){.s = "backslash before newline: \\\nnext line"}),
    ((CVal){.s = "trailing spaces  \nnext"}),
    ((CVal){.s = "C++ empty delimiter collision: )\"\nvalue"}),
    ((CVal){.s = "C++ first fallback collision: )\" and )x\"\nvalue"}),
    ((CVal){.s = "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue"}),
    ((CVal){.s = "Rust delimiter collision: \"#\nvalue"}),
    ((CVal){.s = "Lua delimiter collision: ]]\nvalue"}),
    ((CVal){.s = "Swift delimiter collision: \"\"\"#\nvalue"}),
    ((CVal){.s = "Swift interpolation collision: \\#(value)\nvalue"}),
    ((CVal){.s = "Ruby fallback interpolation  \n#{expression} #@instance #$global"}),
    ((CVal){.s = "NUL followed by a digit: \0007"}),
    ((CVal){.s = "carriage\rreturn"}),
}});
    (void)my_data;
    return 0;
}
