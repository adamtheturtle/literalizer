#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
process(@"hello");
process(@42);
process(@YES);
}
    return 0;
}
