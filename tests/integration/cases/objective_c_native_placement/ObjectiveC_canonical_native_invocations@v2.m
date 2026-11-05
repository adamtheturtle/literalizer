#import <Foundation/Foundation.h>
@interface PlacementWitness : NSObject
- (double)cost:(NSString *)name
    includingEstimatedRuntimeInMilliseconds:(double)value;
@end
@implementation PlacementWitness
- (double)cost:(NSString *)name
    includingEstimatedRuntimeInMilliseconds:(double)value {
  NSCAssert([name isEqualToString:@"é😀"], @"native string changed");
  return value;
}
@end
static void verifyCost(double actual, NSArray *expected) {
  NSCAssert(actual == [expected[0] doubleValue],
            @"nested selector call changed");
}
static void verifyNumbers(NSInteger integer, double real) {
  NSCAssert(integer == 42 && real == 7.5, @"native scalar types changed");
}
static NSDictionary<NSString *, NSArray<NSString *> *> *makeGroups(void) {
  return @{@"team" : @[ @"native" ]};
}
int main(void) {
  @autoreleasepool {
    NSArray<NSDictionary<NSString *, id> *> *rows = @[
      @{
        @"name" :
            @"a long escaped value with a quote \" and Unicode café 😀 abcdefgh"
            @"ij abcdefghij abcdefghij abcdefghij abcdefghij abcdefghij abcdefg"
            @"hij abcdefghij abcdefghij abcdefghij",
        @"count" : @42,
      },
      @{
        @"name" : @"second",
        @"count" : @2,
      },
    ];
    PlacementWitness *witness = [[PlacementWitness alloc] init];
    double inlineResult = [witness cost:@"é😀"
        includingEstimatedRuntimeInMilliseconds:7.5];
    verifyCost(
        [witness cost:@"é😀" includingEstimatedRuntimeInMilliseconds:7.5], @[
          @7.5,
          @"a nested call with a long selector",
        ]);
    verifyNumbers(42, 7.5);
    id value_with_a_long_identifier_used_to_check_assignment_wrapping_here =
        @9223372036854775807;
    NSDictionary<NSString *, NSArray<NSString *> *> *groupNames = makeGroups();
    NSArray<NSString *> *setEntries = @[
      @"alpha",
      @"beta",
    ];
    NSCAssert(setEntries.count == 2 && [setEntries containsObject:@"beta"],
              @"delimiter-free set changed");
    NSCAssert(rows.count == 2 && [rows[1][@"count"] integerValue] == 2,
              @"collection changed");
    NSCAssert(
        [rows[0][@"name"]
            isEqualToString:
                @"a long escaped value with a quote \" and Unicode café 😀 "
                @"abcdefghij abcdefghij abcdefghij abcdefghij abcdefghij "
                @"abcdefghij abcdefghij abcdefghij abcdefghij abcdefghij"],
        @"escaping or string layout changed");
    NSCAssert(
        [value_with_a_long_identifier_used_to_check_assignment_wrapping_here
            longLongValue] == 9223372036854775807LL,
        @"long binding changed");
    NSCAssert([groupNames[@"team"][0] isEqualToString:@"native"],
              @"generic binding changed");
    NSCAssert(inlineResult == 7.5, @"inline message result changed");
  }
  return 0;
}
