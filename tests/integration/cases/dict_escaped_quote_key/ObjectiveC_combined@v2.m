#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a\"b": @1,
};
(void)my_data;
my_data = @{
    @"a\"b": @1,
};
    (void)my_data;
}
    return 0;
}
