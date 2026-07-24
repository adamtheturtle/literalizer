#import <Foundation/Foundation.h>
static id process(id _a0) { (void)_a0; return nil; }
static void emit(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
emit(process(@42), 1);
}
    return 0;
}
