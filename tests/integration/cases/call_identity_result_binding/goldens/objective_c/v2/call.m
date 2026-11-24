#import <Foundation/Foundation.h>
static id kThing_go_stub_(id _a0) { (void)_a0; return nil; }
struct kThingType_ { id (*go)(id); };
static const struct kThingType_ kThing = { .go = kThing_go_stub_ };
int main(void) {
@autoreleasepool {
id my_data = kThing.go(@[]);
    (void)my_data;
}
    return 0;
}
