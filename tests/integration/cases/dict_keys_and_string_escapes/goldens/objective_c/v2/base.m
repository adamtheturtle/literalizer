#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"plain": @[@1, @2],
    @"with-dash": @"a\nb",
};
    (void)my_data;
}
    return 0;
}
