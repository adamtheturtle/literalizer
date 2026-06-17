#import <Foundation/Foundation.h>
static id record_value(id _a0) { (void)_a0; return nil; }
static void flush_buffer(id _a0) { (void)_a0; }
static void emit(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
emit(record_value(@42));
flush_buffer(@3);
}
    return 0;
}
