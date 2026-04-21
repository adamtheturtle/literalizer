#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
static void obj_api_client_post_stub_() {}
struct clientType_ { void (*post)(); };
struct apiType_ { struct clientType_ client; };
struct objType_ { struct apiType_ api; };
static const struct objType_ obj = { .api = { .client = { .post = obj_api_client_post_stub_ } } };
void check_(void) {
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(((CVal){.b = true}));
}
