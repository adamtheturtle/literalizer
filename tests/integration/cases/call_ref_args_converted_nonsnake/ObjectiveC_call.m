#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id myVar = @[
    @1,
    @2,
    @3,
];
id myOther = @[
    @4,
    @5,
    @6,
];
process(myVar, @42);
process(myOther, @7);
}
    return 0;
}
