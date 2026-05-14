#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"name": @"Alice",
    @"tags": [NSSet setWithArray:@[
        @YES,
        @42,
        @"apple",
    ]],
};
    (void)my_data;
}
    return 0;
}
