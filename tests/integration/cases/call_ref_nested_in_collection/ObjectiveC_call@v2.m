#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id big_list = @[
    @"x",
];
process(@{@"k": big_list}, @{@"m": big_list});
}
    return 0;
}
