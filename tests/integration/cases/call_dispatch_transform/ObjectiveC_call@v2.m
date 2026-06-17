#import <Foundation/Foundation.h>
static id record(id _a0) { (void)_a0; return nil; }
static void flush(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
record(@42);
flush(@3);
}
    return 0;
}
