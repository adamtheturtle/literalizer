#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id myVar = @{
    @"_": @"_",
};
id my_data = @{
    @"key": myVar,
};
    (void)my_data;
}
    return 0;
}
