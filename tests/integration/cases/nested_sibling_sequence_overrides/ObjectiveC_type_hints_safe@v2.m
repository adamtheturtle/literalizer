#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @[@[@1], @[@2]],
    @"b": @[@[@"x"], @[@"y"]],
};
    (void)my_data;
}
    return 0;
}
