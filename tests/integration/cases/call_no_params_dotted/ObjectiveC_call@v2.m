#import <Foundation/Foundation.h>
static void kThrottler_check_stub_(void) {}
struct kThrottlerType_ { void (*check)(void); };
static const struct kThrottlerType_ kThrottler = { .check = kThrottler_check_stub_ };
int main(void) {
@autoreleasepool {
kThrottler.check();
kThrottler.check();
}
    return 0;
}
