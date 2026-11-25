#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"numbers": @[@1, @2],
    @"nested": @{@"inner": @[@3]},
    @"mixed": @[@4, @"five"],
};
    (void)my_data;
}
    return 0;
}
