#import <Foundation/Foundation.h>
@interface NativeCounter : NSObject {
    NSInteger _count;
}
- (instancetype)initWithCount:(NSInteger)count;
- (BOOL)shouldSendNotification:(NSString *)userId notificationTimestamp:(double)timestamp;
- (void)reset;
- (NSInteger)count;
+ (NSString *)label;
- (NSInteger)a:(NSInteger)a veryLongSecondParameterName:(NSInteger)b;
@end
@implementation NativeCounter
- (NSInteger)a:(NSInteger)a veryLongSecondParameterName:(NSInteger)b { return a + b; }
- (instancetype)initWithCount:(NSInteger)count {
    self = [super init];
    if (self) { _count = count; }
    return self;
}
- (BOOL)shouldSendNotification:(NSString *)userId notificationTimestamp:(double)timestamp {
    _count++;
    return [userId isEqualToString:@"user_1"] && timestamp == 100.0;
}
- (void)reset { _count = 0; }
- (NSInteger)count { return _count; }
+ (NSString *)label { return @"native"; }
@end
static void verifyResult(BOOL actual, NSArray *expected) {
    NSCAssert(actual == [expected[0] boolValue], @"wrong selector result");
}
static void verifyObject(NSNumber *actual) {
    NSCAssert([actual boolValue], @"scalar call result must be boxed");
}
static void verifyBoxes(NSNumber *number, NSNumber *flag) {
    NSCAssert([number integerValue] == 42 && [flag boolValue], @"object arguments must be boxed");
}
static NSArray<NSString *> *makeNames(void) { return @[@"native"]; }
static void verifyNull(id value) { NSCAssert(value == [NSNull null], @"null changed"); }
static void verifyBool(BOOL value) { NSCAssert(value, @"bool must stay scalar"); }
static void verifyScalar(NSInteger value) { NSCAssert(value == 42, @"integer changed"); }
static void verifyDouble(double value) { NSCAssert(value == 3.0, @"numeric widening changed"); }
static void verifyLabel(NSString *value) { NSCAssert([value isEqualToString:@"native"], @"id reference changed"); }
static void verifyDictionary(NSDictionary<NSString *, NSArray<NSString *> *> *value) {
    NSCAssert([value[@"group"][0] isEqualToString:@"native"], @"generic values changed");
}
int main(void) {
    @autoreleasepool {
    NativeCounter *counter =
      [[NativeCounter alloc] initWithCount:5];
    BOOL allowed = [counter shouldSendNotification:@"user_1"
                             notificationTimestamp:100.0];
    verifyObject(@(allowed));
    allowed =
        [counter shouldSendNotification:@"user_2"
            notificationTimestamp:101.0];
    verifyResult([counter shouldSendNotification:@"user_1"
                           notificationTimestamp:100.0],
                 @[
                   @YES,
                   @"native selector",
                 ]);
    verifyObject(@([counter shouldSendNotification:@"user_1"
                             notificationTimestamp:100.0]));
    NSString *label = [NativeCounter label];
    verifyBoxes(
      @42,
      @YES);
    [counter reset];
    NSInteger finalCount = [counter count];
    NSInteger nestedCount = [[[NativeCounter alloc] initWithCount:3] count];
    NSArray<NSString *> *names = makeNames();
    NSMutableArray<NSString *> *mutableNames =
      [@[
      @"native",
    ] mutableCopy];
    verifyNull([NSNull null]);
    verifyBool(YES);
    verifyDictionary(@{
      @"group": @[
        @"native",
      ],
    });
    verifyScalar(42);
    verifyDouble((double)nestedCount);
    verifyLabel(label);
    verifyScalar([counter
                                             a:40
                   veryLongSecondParameterName:2]);
        [mutableNames addObject:@"second"];
        NSCAssert(mutableNames.count == 2, @"literal receiver lost mutability");
        NSCAssert(!allowed, @"reassignment must call the original receiver");
        NSCAssert([label isEqualToString:@"native"], @"class message changed");
        NSCAssert(finalCount == 0 && nestedCount == 3, @"constructor or reset changed");
        NSCAssert([names[0] isEqualToString:@"native"], @"generic binding changed");
    }
    return 0;
}
