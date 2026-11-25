#import <Foundation/Foundation.h>
static id kOuter_thing_go_stub_(void) { return nil; }
struct thingType_ { id (*go)(void); };
struct kOuterType_ { struct thingType_ thing; };
static const struct kOuterType_ kOuter = { .thing = { .go = kOuter_thing_go_stub_ } };
int main(void) {
@autoreleasepool {
kOuter.thing.go();
}
    return 0;
}
