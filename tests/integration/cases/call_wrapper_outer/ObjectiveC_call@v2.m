#import <Foundation/Foundation.h>
static id process(id _a0) { (void)_a0; return nil; }
static void emit(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
emit(process(@42));
}
    return 0;
}
