#import <Foundation/Foundation.h>
static void consume(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id shared = @42;
consume(shared);
}
    return 0;
}
