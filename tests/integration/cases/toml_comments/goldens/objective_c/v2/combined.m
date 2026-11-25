#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    // before
    @"answer": @42,  // inline
    @"plain": @"ok",
    // trailing
};
(void)my_data;
my_data = @{
    // before
    @"answer": @42,  // inline
    @"plain": @"ok",
    // trailing
};
    (void)my_data;
}
    return 0;
}
