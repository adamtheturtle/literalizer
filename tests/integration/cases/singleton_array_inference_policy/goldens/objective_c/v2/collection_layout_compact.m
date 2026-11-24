#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"below": @[@[@[@[@[@[@[@[@1]]]]]]]],
    @"boundary": @[@[@[@[@[@[@[@[@[@2]]]]]]]]],
    @"multiple": @[@[@[@[@[@[@[@[@[@[@[@[@[@[@[@[@[@3]]]]]]]]]]]]]]]]],
    @"text": @[@[@[@[@[@[@[@[@[@"value"]]]]]]]]],
    @"boolean": @[@[@[@[@[@[@[@[@[@YES]]]]]]]]],
    @"float": @[@[@[@[@[@[@[@[@[@1.5]]]]]]]]],
};
    (void)my_data;
}
    return 0;
}
