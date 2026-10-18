#import <Foundation/Foundation.h>
static void kApp_go_stub_(id _a0, id _a1) { (void)_a0, (void)_a1; }
struct kAppType_ { void (*go)(id, id); };
static const struct kAppType_ kApp = { .go = kApp_go_stub_ };
int main(void) {
@autoreleasepool {
kApp.go(@[@1], @[@"text"]);
}
    return 0;
}
