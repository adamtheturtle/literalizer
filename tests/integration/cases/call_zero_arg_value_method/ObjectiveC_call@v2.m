#import <Foundation/Foundation.h>
static id kThing_go_stub_(void) { return nil; }
struct kThingType_ { id (*go)(void); };
static const struct kThingType_ kThing = { .go = kThing_go_stub_ };
int main(void) {
@autoreleasepool {
kThing.go();
}
    return 0;
}
