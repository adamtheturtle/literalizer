#import <Foundation/Foundation.h>
static void consume(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
consume(@(-2147483649));
consume(@2147483648);
}
    return 0;
}
