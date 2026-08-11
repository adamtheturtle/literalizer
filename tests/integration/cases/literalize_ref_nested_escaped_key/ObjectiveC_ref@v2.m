#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id foo = @{
    @"_": @"_",
};
id my_data = @{
    @"items": @[@{@"other": @1}, foo],
    @"mapping": @{@"value": foo},
};
    (void)my_data;
}
    return 0;
}
