#import <Foundation/Foundation.h>
static void consume(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id my_null = [NSNull null];
id regular_null = [NSNull null];
consume(my_null);
consume(regular_null);
}
    return 0;
}
