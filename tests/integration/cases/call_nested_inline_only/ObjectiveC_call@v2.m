#import <Foundation/Foundation.h>
static void f(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
f(@2, @"hello");  // trailing note
f(@3, @"world");  // another note
}
    return 0;
}
