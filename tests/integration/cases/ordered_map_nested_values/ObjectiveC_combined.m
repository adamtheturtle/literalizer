#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"name": @"Alice",
    @"scores": @{@"1": @"first", @"2": @"second"},
};
(void)my_data;
my_data = @{
    @"name": @"Alice",
    @"scores": @{@"1": @"first", @"2": @"second"},
};
    (void)my_data;
}
    return 0;
}
