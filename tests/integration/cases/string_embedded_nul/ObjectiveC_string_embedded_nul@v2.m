#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"x": @"\000",
    @"y": @"\0001",
};
    (void)my_data;
}
    return 0;
}
