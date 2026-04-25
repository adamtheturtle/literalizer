#import <Foundation/Foundation.h>
void check_(void) {
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
