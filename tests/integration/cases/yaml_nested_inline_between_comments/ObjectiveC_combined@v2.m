#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @[@2, @"hello"],  // trailing note
    // next element
    @[@3, @"world"],
];
(void)my_data;
my_data = @[
    @[@2, @"hello"],  // trailing note
    // next element
    @[@3, @"world"],
];
    (void)my_data;
}
    return 0;
}
