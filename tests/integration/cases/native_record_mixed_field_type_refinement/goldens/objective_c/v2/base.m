#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"first": @{@"items": @[@1, @{@"value": @2}]},
    @"second": @{@"items": @[@1, @{@"value": @"s"}]},
};
    (void)my_data;
}
    return 0;
}
