#import <Foundation/Foundation.h>
static void consume(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id foo = @42;
consume(@[
    @{
        @"other": @1,
    },
    foo,
], @{
    @"left": foo,
    @"other": @1,
});
}
    return 0;
}
