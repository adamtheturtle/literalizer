#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id siblingMap = @{
    @"k": @2,
};
id my_data = @[
    @{@"k": @1},
    siblingMap,
];
    (void)my_data;
}
    return 0;
}
