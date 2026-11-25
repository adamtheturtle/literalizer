#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id stringMap = @{
    @"k": @"s",
};
id my_data = @[
    stringMap,
    @{@"k": @1},
];
    (void)my_data;
}
    return 0;
}
