#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id sharedValues = @[
    @1,
    @2,
];
id my_data = @{
    @"a": sharedValues,
};
(void)my_data;
my_data = @{
    @"a": sharedValues,
};
    (void)my_data;
}
    return 0;
}
