#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"first": @[@[@1, @"value"], @[]],
    @"second": @[@[], @[@2, @"other"]],
};
    (void)my_data;
}
    return 0;
}
