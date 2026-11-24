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
struct Record1 { const char *kind; const char *pr_id; };
struct Record0 { const char *name; struct Record1 input; CVal expected; };
int main(void) {
struct Record0 my_data[] = {
    (struct Record0){
        .name = "test_1",
        .input = (struct Record1){
            .kind = "create",
            .pr_id = "pr_1",
        },
        .expected = ((CVal){.m = (CKV[]){
            {"pr_id", ((CVal){.s = "pr_1"})},
            {"status", ((CVal){.s = "draft"})},
        }}),
    },
    (struct Record0){
        .name = "test_2",
        .input = (struct Record1){
            .kind = "publish",
            .pr_id = "pr_1",
        },
        .expected = ((CVal){.m = (CKV[]){
            {"error", ((CVal){.s = "invalid_operation"})},
        }}),
    },
};
    (void)my_data;
    return 0;
}
