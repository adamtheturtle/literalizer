#import <Foundation/Foundation.h>
static id process(id _a0) { (void)_a0; return nil; }
int main(void) {
@autoreleasepool {
process(@"hello");
process(@42);
process(@YES);
}
    return 0;
}
