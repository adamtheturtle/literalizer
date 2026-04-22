#import <Foundation/Foundation.h>
static void obj_api_client_post_stub_(id _a0) {}
struct clientType_ { void (*post)(id); };
struct apiType_ { struct clientType_ client; };
struct objType_ { struct apiType_ api; };
static const struct objType_ obj = { .api = { .client = { .post = obj_api_client_post_stub_ } } };
void check_(void) {
obj.api.client.post(@"hello");
obj.api.client.post(@(42));
obj.api.client.post(@YES);
}
