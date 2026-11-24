#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"test": @[@5, @[@"compile", @"test"]],
    @"package": @[@7, @[@"link", @"test"]],
};
    (void)my_data;
}
    return 0;
}
