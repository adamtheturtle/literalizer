#import <Foundation/Foundation.h>
static void kApp_client_go_stub_(id _a0, id _a1) { (void)_a0, (void)_a1; }
struct clientType_ { void (*go)(id, id); };
struct kAppType_ { struct clientType_ client; };
static const struct kAppType_ kApp = { .client = { .go = kApp_client_go_stub_ } };
int main(void) {
@autoreleasepool {
kApp.client.go(@[@1], @[@2]);
}
    return 0;
}
