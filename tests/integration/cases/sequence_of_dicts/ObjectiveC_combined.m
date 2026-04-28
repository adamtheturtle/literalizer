#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @{@"name": @"Alice", @"age": @30},
    @{@"name": @"Bob", @"age": @25},
];
(void)my_data;
my_data = @[
    @{@"name": @"Alice", @"age": @30},
    @{@"name": @"Bob", @"age": @25},
];
    (void)my_data;
    return 0;
}
