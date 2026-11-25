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
    {"ancient_date", ((CVal){.s = "1500-03-01"})},
    {"modern_date", ((CVal){.s = "2024-01-15"})},
    {"before_date", ((CVal){.s = "1582-10-04"})},
    {"gap_date", ((CVal){.s = "1582-10-10"})},
    {"transition_date", ((CVal){.s = "1582-10-15"})},
    {"after_date", ((CVal){.s = "1582-10-16"})},
    {"before_naive", ((CVal){.s = "1582-10-04T12:30:00.000001"})},
    {"gap_naive", ((CVal){.s = "1582-10-10T12:30:00.500000"})},
    {"transition_positive", ((CVal){.s = "1582-10-15T00:30:00+18:00"})},
    {"transition_negative", ((CVal){.s = "1582-10-15T23:30:00-18:00"})},
    {"after_positive", ((CVal){.s = "1582-10-16T00:30:00+18:00"})},
}});
    (void)my_data;
    return 0;
}
