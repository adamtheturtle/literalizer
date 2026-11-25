#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a_b": @1,
    @"a-b": @2,
    @"averyveryverylongkeynamethatgoesonandonandon": @3,
    @"averyveryverylongkeynamethatgoesonandmore": @4,
};
    (void)my_data;
}
    return 0;
}
