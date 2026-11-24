#import <Foundation/Foundation.h>
static void f(id _a0, id _a1) { (void)_a0, (void)_a1; }
int main(void) {
@autoreleasepool {
// calls heading
// before call one
// first argument
f(@1, @2);  // after call one
// second argument
f(@3, @4);
// after all calls
}
    return 0;
}
