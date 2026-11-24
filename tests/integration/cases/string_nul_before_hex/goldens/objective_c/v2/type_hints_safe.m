#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"x": @"before\000after",
};
    (void)my_data;
}
    return 0;
}
