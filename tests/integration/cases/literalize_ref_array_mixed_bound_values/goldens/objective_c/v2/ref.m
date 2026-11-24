#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id arrayValue = @[
    @1,
    @2,
];
id scalarValue = @3;
id my_data = @[
    arrayValue,
    scalarValue,
];
    (void)my_data;
}
    return 0;
}
