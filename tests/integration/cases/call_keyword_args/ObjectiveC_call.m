#import <Foundation/Foundation.h>
static id kThrottler_check_stub_(id _a0, id _a1) { (void)_a0; (void)_a1; return nil; }
struct kThrottlerType_ { id (*check)(id, id); };
static const struct kThrottlerType_ kThrottler = { .check = kThrottler_check_stub_ };
static void emit(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
emit(kThrottler.check(@"user_1", @1000.0));
emit(kThrottler.check(@"user_2", @2000.5));
}
    return 0;
}
