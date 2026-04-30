#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id shared = @1;
id other = @2;
process(shared, @1);
process(other, @0);
process(shared, @8);
}
    return 0;
}
