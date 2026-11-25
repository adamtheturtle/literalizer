#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @[@[@1, @2], @[@3]],
    @"b": @[@[], @[@1]],
};
    (void)my_data;
}
    return 0;
}
