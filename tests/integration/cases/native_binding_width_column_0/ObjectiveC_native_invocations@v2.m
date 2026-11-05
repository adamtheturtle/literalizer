#import <Foundation/Foundation.h>
static NSUInteger calls = 0;
static BOOL emitValues(NSString *first, NSString *second) {
    NSCAssert([first isEqualToString:@"first"], @"first argument changed");
    NSCAssert([second isEqualToString:@"second"], @"second argument changed");
    calls++;
    return YES;
}
int main(void) {
    @autoreleasepool {
emitValues(@"first", @"second");
BOOL allowed = emitValues(@"first",
                          @"second");
        NSCAssert(allowed && calls == 2, @"bound call did not execute");
    }
    return 0;
}
