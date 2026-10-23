#import <Foundation/Foundation.h>
static void kProcess_api_fetch_stub_(id _a0) { (void)_a0; }
struct apiType_ { void (*fetch)(id); };
struct kProcessType_ { struct apiType_ api; };
static const struct kProcessType_ kProcess = { .api = { .fetch = kProcess_api_fetch_stub_ } };
int main(void) {
@autoreleasepool {
kProcess.api.fetch(@{@"data": @"hello"});
kProcess.api.fetch(@{@"data": @42});
kProcess.api.fetch(@{@"data": @YES});
}
    return 0;
}
