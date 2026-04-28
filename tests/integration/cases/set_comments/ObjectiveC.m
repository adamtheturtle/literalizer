#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = [NSSet setWithArray:@[
    @"apple",  // inline comment
    // before banana
    @"banana",
    // trailing
]];
    (void)my_data;
}
    return 0;
}
