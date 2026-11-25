#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"single_map": @[@{}],
    @"single_list": @[@[@1]],
    @"single_deep": @[@[@[@2]]],
};
    (void)my_data;
}
    return 0;
}
