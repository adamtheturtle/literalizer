#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
process([NSNull null]);
process(@[@1, @2]);
}
    return 0;
}
