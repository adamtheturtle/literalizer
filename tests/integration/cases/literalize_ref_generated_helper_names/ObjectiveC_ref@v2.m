#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id std = @{
    @"a": @1,
};
id arena = @{
    @"a": @1,
};
id allocator = @{
    @"a": @1,
};
id my_data = @[
    std,
    arena,
    allocator,
];
    (void)my_data;
}
    return 0;
}
