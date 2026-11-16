#import <Foundation/Foundation.h>
#include <assert.h>
static int *event_index(void) { static int index = 0; return &index; }
static void observe_event(long long actual) {
    const long long expected[] = {1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42};
    assert(*event_index() < 12 && actual == expected[*event_index()]);
    ++*event_index();
}
static NSNumber *process(NSNumber *argument) { observe_event(1); observe_event(argument.longLongValue); return @(argument.longLongValue + 100); }
static void emit(NSNumber *argument0, NSNumber *argument1) { observe_event(2); observe_event(argument0.longLongValue); observe_event(3); observe_event(argument1.longLongValue); }
static void verify_events(void) { assert(*event_index() == 12); }
int main(void) {
@autoreleasepool {
emit(process(@1), @41);
emit(process(@2), @42);
verify_events();
}
    return 0;
}
