#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id emptyValues = @[];
id integerValues = @[
    @1,
];
id floatValues = @[
    @1.5,
];
id my_data = @[
    emptyValues,
    integerValues,
    floatValues,
];
    (void)my_data;
}
    return 0;
}
