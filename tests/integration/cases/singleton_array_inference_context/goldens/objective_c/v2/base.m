#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"nil": @[@[@[@[@[@[@[@[@[[NSNull null]]]]]]]]]],
    @"empty": @[@[@[@[@[@[@[@[@[@[]]]]]]]]]],
    @"siblings": @[@[@[@[@[@[@[@[@[@[@4, @5]]]]]]]]]],
};
    (void)my_data;
}
    return 0;
}
