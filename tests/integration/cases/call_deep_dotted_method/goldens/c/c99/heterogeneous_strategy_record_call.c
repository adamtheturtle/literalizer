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
static void obj_api_client_post_stub_(CVal _a0) { (void)_a0; }
struct clientType_ { void (*post)(CVal); };
struct apiType_ { struct clientType_ client; };
struct objType_ { struct apiType_ api; };
static const struct objType_ obj = { .api = { .client = { .post = obj_api_client_post_stub_ } } };
int main(void) {
obj.api.client.post(((CVal){.s = "hello"}));
obj.api.client.post(((CVal){.i = 42}));
obj.api.client.post(((CVal){.b = true}));
    return 0;
}
