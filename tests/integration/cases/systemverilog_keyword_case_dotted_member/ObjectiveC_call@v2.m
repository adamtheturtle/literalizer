#import <Foundation/Foundation.h>
static void kThing_Before_stub_(id _a0) { (void)_a0; }
struct kThingType_ { void (*Before)(id); };
static const struct kThingType_ kThing = { .Before = kThing_Before_stub_ };
int main(void) {
@autoreleasepool {
kThing.Before(@1);
}
    return 0;
}
