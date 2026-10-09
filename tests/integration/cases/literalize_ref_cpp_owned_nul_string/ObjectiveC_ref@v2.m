#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id shared = @"a\000b";
id my_data = @{
    @"value": shared,
};
    (void)my_data;
}
    return 0;
}
