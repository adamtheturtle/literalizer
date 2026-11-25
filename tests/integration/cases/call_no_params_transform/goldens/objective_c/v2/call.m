#import <Foundation/Foundation.h>
static id process(void) { return nil; }
static void emit(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
emit(process());
emit(process());
}
    return 0;
}
