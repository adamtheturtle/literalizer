#import <Foundation/Foundation.h>
static id process(id _a0) { (void)_a0; return nil; }
static void emit(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
emit(process(@"hello"), @{@"a": @1, @"b": @2});
emit(process(@42), @{@"c": @3, @"d": @4});
}
    return 0;
}
