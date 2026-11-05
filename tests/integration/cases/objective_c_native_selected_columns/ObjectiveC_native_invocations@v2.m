#import <Foundation/Foundation.h>
static NSMutableArray *received(void) {
    static NSMutableArray *values = nil;
    if (values == nil) { values = [NSMutableArray array]; }
    return values;
}
static void consume(id value) { [received() addObject:value]; }
int main(void) {
    @autoreleasepool {
        consume(@"first");
        consume(@42);
        NSArray *expected = @[@"first", @42];
        NSCAssert([received() isEqualToArray:expected], @"selected native values changed");
    }
    return 0;
}
