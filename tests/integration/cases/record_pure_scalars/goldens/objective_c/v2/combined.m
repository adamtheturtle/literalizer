#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"name": @"Alice",
    @"age": @30,
    @"active": @YES,
    @"score": @4.5,
};
(void)my_data;
my_data = @{
    @"name": @"Alice",
    @"age": @30,
    @"active": @YES,
    @"score": @4.5,
};
    (void)my_data;
}
    return 0;
}
