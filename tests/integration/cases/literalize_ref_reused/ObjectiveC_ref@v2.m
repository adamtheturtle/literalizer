#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id sharedVar = @{
    @"_": @"_",
};
id my_data = @[
    sharedVar,
    sharedVar,
];
    (void)my_data;
}
    return 0;
}
