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
    {"true_to_one", ((CVal){.m = (CKV[]){{"value", ((CVal){.i = 1})}}})},
    {"one_to_true", ((CVal){.m = (CKV[]){{"value", ((CVal){.b = true})}}})},
    {"false_to_zero", ((CVal){.m = (CKV[]){{"value", ((CVal){.i = 0})}}})},
    {"zero_to_false", ((CVal){.m = (CKV[]){{"value", ((CVal){.b = false})}}})},
    {"nested_boolean_to_float", ((CVal){.m = (CKV[]){{"value", ((CVal){.a = (CVal[]){((CVal){.f = 1.0})}})}}})},
    {"nested_float_to_boolean", ((CVal){.m = (CKV[]){{"value", ((CVal){.a = (CVal[]){((CVal){.b = false})}})}}})},
    {"nested_value_types_changed", ((CVal){.m = (CKV[]){{"value", ((CVal){.m = (CKV[]){{"nested", ((CVal){.a = (CVal[]){((CVal){.b = true}), ((CVal){.i = 0})}})}}})}}})},
    {"nested_value_types_reversed", ((CVal){.m = (CKV[]){{"value", ((CVal){.m = (CKV[]){{"nested", ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.b = false})}})}}})}}})},
    {"array_order_changed", ((CVal){.m = (CKV[]){{"value", ((CVal){.a = (CVal[]){((CVal){.i = 2}), ((CVal){.i = 1})}})}}})},
    {"array_length_changed", ((CVal){.m = (CKV[]){{"value", ((CVal){.a = (CVal[]){((CVal){.i = 1}), ((CVal){.i = 2})}})}}})},
    {"null_to_zero", ((CVal){.m = (CKV[]){{"value", ((CVal){.i = 0})}}})},
    {"string_to_boolean", ((CVal){.m = (CKV[]){{"value", ((CVal){.b = true})}}})},
    {"object_key_changed", ((CVal){.m = (CKV[]){{"value", ((CVal){.m = (CKV[]){{"b", ((CVal){.i = 1})}}})}}})},
}});
    (void)my_data;
    return 0;
}
