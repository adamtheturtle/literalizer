#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"call": @"send", @"args": @[@1, @"email", @"a@gmail.com", @100]},
    @{@"call": @"recv", @"args": @[@2, @"sms", @"b@example.com", @200]},
];
    (void)my_data;
}
    return 0;
}
