#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"lint": @[@2, @[]],
    @"test": @[@5, @[@"compile"]],
    @"package": @[@7, @[@"link", @"test"]],
};
    (void)my_data;
}
    return 0;
}
