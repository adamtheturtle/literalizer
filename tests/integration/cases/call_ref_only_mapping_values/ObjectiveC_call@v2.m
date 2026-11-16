#import <Foundation/Foundation.h>
static void consume(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id item = @42;
consume(@{@"field": item});
}
    return 0;
}
