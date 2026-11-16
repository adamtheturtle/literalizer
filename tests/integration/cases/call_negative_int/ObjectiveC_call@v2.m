#import <Foundation/Foundation.h>
#include <assert.h>
static int *event_index(void) { static int index = 0; return &index; }
static void observe_event(long long actual) {
    const long long expected[] = {1, -1, 1, -2, 1, -3};
    assert(*event_index() < 6 && actual == expected[*event_index()]);
    ++*event_index();
}
static NSNumber *process(NSNumber *argument) { observe_event(1); observe_event(argument.longLongValue); return @(argument.longLongValue + 100); }
static void verify_events(void) { assert(*event_index() == 6); }
int main(void) {
@autoreleasepool {
process(@(-1));
process(@(-2));
process(@(-3));
verify_events();
}
    return 0;
}
