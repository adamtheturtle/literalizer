#import <Foundation/Foundation.h>
@interface Counter : NSObject
@property(nonatomic) NSUInteger calls;
- (BOOL)accept:(NSString *)user timestamp:(double)timestamp;
@end
@implementation Counter
- (BOOL)accept:(NSString *)user timestamp:(double)timestamp {
    self.calls++;
    return [user isEqualToString:@"user_1"] && timestamp == 100.0;
}
@end
static NSUInteger checks = 0;
static void checkResult(BOOL actual, NSArray *expected) {
    NSCAssert(actual == [expected[0] boolValue], @"result changed");
    NSCAssert([expected[1] isEqualToString:@"first"], @"expected row changed");
    checks++;
}
int main(void) {
    @autoreleasepool {
        Counter *counter = [[Counter alloc] init];
        checkResult([counter accept:@"user_1" timestamp:100.0], @[
            @YES,
            @"first",
        ]);
        NSCAssert(counter.calls == 1 && checks == 1, @"native call was skipped");
    }
    return 0;
}
