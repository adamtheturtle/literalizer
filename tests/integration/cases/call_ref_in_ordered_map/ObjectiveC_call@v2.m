#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id big_list = @[
    @"x",
];
process(@{@"m": big_list});
}
    return 0;
}
