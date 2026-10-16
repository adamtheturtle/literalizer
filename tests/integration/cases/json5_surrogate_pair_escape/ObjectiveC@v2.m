#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"astral": @"😀",
    @"mixed": @"a😀b",
    @"count": @2,
    @"list": @[@"😀", @1],
    @"nested": @{@"inner": @"😀"},
};
    (void)my_data;
}
    return 0;
}
