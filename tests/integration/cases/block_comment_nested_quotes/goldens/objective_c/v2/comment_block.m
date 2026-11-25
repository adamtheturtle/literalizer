#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    /* "{-" and '{-' stay readable */
    /* balanced {- nested -} and trailing -} stay readable */
    @"x": @1,
};
    (void)my_data;
}
    return 0;
}
