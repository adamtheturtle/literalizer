#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"lists": @[@[@1], @[@"x"], @[]],
    @"maps": @[@{@"x": @1}, @{@"x": @"s"}],
    @"empties": @{@"a": @[@1], @"b": @[]},
};
    (void)my_data;
}
    return 0;
}
