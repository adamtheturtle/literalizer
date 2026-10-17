#import <Foundation/Foundation.h>
static void kThing_first_value_stub_(id _a0) { (void)_a0; }
struct kThingType_ { void (*first_value)(id); };
static const struct kThingType_ kThing = { .first_value = kThing_first_value_stub_ };
int main(void) {
@autoreleasepool {
kThing.first_value(@1);
}
    return 0;
}
