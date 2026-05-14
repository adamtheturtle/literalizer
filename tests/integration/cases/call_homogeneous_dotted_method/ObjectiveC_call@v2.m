#import <Foundation/Foundation.h>
static void kApp_client_fetch_stub_(id _a0) { (void)_a0; }
struct clientType_ { void (*fetch)(id); };
struct kAppType_ { struct clientType_ client; };
static const struct kAppType_ kApp = { .client = { .fetch = kApp_client_fetch_stub_ } };
int main(void) {
@autoreleasepool {
kApp.client.fetch(@"hello");
kApp.client.fetch(@"world");
}
    return 0;
}
