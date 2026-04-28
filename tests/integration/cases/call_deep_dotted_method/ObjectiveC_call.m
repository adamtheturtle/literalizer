#import <Foundation/Foundation.h>
static void kObj_api_client_post_stub_(id _a0) { (void)_a0; }
struct clientType_ { void (*post)(id); };
struct apiType_ { struct clientType_ client; };
struct kObjType_ { struct apiType_ api; };
static const struct kObjType_ kObj = { .api = { .client = { .post = kObj_api_client_post_stub_ } } };
int main(void) {
kObj.api.client.post(@"hello");
kObj.api.client.post(@42);
kObj.api.client.post(@YES);
    return 0;
}
