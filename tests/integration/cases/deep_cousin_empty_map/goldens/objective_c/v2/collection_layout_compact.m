#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"outer": @{@"inner": @{@"x": @1}}},
    @{@"outer": @{@"inner": @{}}},
];
    (void)my_data;
}
    return 0;
}
