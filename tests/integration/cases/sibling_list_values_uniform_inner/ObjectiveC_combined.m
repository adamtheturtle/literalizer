#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"lint": @[@2, @[@1]],
    @"test": @[@5, @[@7]],
};
(void)my_data;
my_data = @{
    @"lint": @[@2, @[@1]],
    @"test": @[@5, @[@7]],
};
    (void)my_data;
}
    return 0;
}
