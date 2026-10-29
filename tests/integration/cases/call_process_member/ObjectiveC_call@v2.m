#import <Foundation/Foundation.h>
static void kApp_process_fetch_stub_(id _a0) { (void)_a0; }
struct processType_ { void (*fetch)(id); };
struct kAppType_ { struct processType_ process; };
static const struct kAppType_ kApp = { .process = { .fetch = kApp_process_fetch_stub_ } };
int main(void) {
@autoreleasepool {
kApp.process.fetch(@{@"data": @"hello"});
kApp.process.fetch(@{@"data": @42});
kApp.process.fetch(@{@"data": @YES});
}
    return 0;
}
