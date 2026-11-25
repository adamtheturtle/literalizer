#import <Foundation/Foundation.h>
static id kThing_go_stub_(id _a0, id _a1, id _a2) { (void)_a0, (void)_a1, (void)_a2; return nil; }
struct kThingType_ { id (*go)(id, id, id); };
static const struct kThingType_ kThing = { .go = kThing_go_stub_ };
int main(void) {
@autoreleasepool {
kThing.go(@[], @[@1], @[]);
kThing.go(@[@"text"], @[@2], @[]);
kThing.go(@[], @[@"text"], @[]);
kThing.go(@[@"text"], @[@2], @[@3]);
}
    return 0;
}
