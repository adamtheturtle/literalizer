#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @{
        @"b": @[@1],
        // Outdented from the sequence, so the inner mapping claims this.
        @"c": @2,
    },
    // Outdented from the inner mapping too, so the root claims this.
    @"d": @3,
};
(void)my_data;
my_data = @{
    @"a": @{
        @"b": @[@1],
        // Outdented from the sequence, so the inner mapping claims this.
        @"c": @2,
    },
    // Outdented from the inner mapping too, so the root claims this.
    @"d": @3,
};
    (void)my_data;
}
    return 0;
}
