#import <Foundation/Foundation.h>
#include <assert.h>
static int event_index = 0;
static void observe_event(long long actual) {
    const long long expected[] = {1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42};
    assert(event_index < 12 && actual == expected[event_index]);
    event_index++;
}
static NSNumber *process(NSNumber *value) { observe_event(1); observe_event(value.longLongValue); return @(value.longLongValue + 100); }
static void emit(NSNumber *actual, NSNumber *zipped) { observe_event(2); observe_event(actual.longLongValue); observe_event(3); observe_event(zipped.longLongValue); }
static void verify_events(void) { assert(event_index == 12); }
int main(void) {
@autoreleasepool {
emit(process(@1), @41);
emit(process(@2), @42);
verify_events();
}
    return 0;
}
