#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    // first dotted key
    // second dotted key
    @"a": @{@"b": @1, @"c": @2},
};
    (void)my_data;
}
    return 0;
}
