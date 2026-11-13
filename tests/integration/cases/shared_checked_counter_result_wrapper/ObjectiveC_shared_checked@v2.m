#import <Foundation/Foundation.h>
#import <Foundation/Foundation.h>
@interface Counter : NSObject
@property(nonatomic) NSUInteger calls;
- (BOOL)accept:(NSString *)user timestamp:(double)timestamp;
@end
@implementation Counter
- (BOOL)accept:(NSString *)user timestamp:(double)timestamp {
    NSCAssert([user isEqualToString:self.calls == 0 ? @"user_1" : @"user_2"], @"receiver user changed");
    NSCAssert(timestamp == 100.0 + self.calls, @"receiver timestamp changed");
    self.calls++;
    return [user isEqualToString:@"user_1"];
}
@end
static NSUInteger checks;
static void checkResult(BOOL actual, NSArray *expected) {
    NSCAssert(actual == [expected[0] boolValue], @"result changed");
    NSCAssert([expected[1] isEqualToString:checks == 0 ? @"first" : @"second"], @"paired reason changed");
    checks++;
}
int main(void) {
    @autoreleasepool {
        Counter *counter = [[Counter alloc] init];
        checkResult([counter accept:@"user_1" timestamp:100.0], @[
            @YES,
            @"first",
        ]);
        NSCAssert(counter.calls == 1 && checks == 1, @"calls skipped");
    }
    return 0;
}
