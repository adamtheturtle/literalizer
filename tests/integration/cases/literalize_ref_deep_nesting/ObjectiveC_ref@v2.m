#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id deep = @{
    @"_": @"_",
};
id my_data = @{
    @"a": @{@"b": @{@"c": deep}},
};
    (void)my_data;
}
    return 0;
}
