#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    // before	line
    @"value": @"left\tright",  // inline	line
    // after	line
};
    (void)my_data;
}
    return 0;
}
