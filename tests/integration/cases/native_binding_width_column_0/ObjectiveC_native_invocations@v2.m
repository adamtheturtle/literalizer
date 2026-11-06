#import <Foundation/Foundation.h>
static NSUInteger *callCount(void) {
    static NSUInteger count = 0;
    return &count;
}
static BOOL emitValues(NSString *first, NSString *second) {
    NSCAssert([first isEqualToString:@"first"], @"first argument changed");
    NSCAssert([second isEqualToString:@"second"], @"second argument changed");
    (*callCount())++;
    return YES;
}
int main(void) {
    @autoreleasepool {
emitValues(@"first", @"second");
BOOL allowed = emitValues(@"first",
                          @"second");
        NSCAssert(allowed && *callCount() == 2, @"bound call did not execute");
    }
    return 0;
}
