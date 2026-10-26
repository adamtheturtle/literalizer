#import <Foundation/Foundation.h>
static void kApi_process_stub_(id _a0) { (void)_a0; }
struct kApiType_ { void (*process)(id); };
static const struct kApiType_ kApi = { .process = kApi_process_stub_ };
int main(void) {
@autoreleasepool {
kApi.process(@{});
}
    return 0;
}
