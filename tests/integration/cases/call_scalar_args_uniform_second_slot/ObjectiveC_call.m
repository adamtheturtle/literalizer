#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
process(@"hello", @"a");
process(@42, @"b");
process(@YES, @"c");
}
    return 0;
}
