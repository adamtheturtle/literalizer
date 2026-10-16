#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    // heading
    @"a": @"single ' // data",
    @"b": @"linecontinuation",
    @"c": @"\\",  // actual comment
    @"d": @"  ",  // final comment
};
    (void)my_data;
}
    return 0;
}
