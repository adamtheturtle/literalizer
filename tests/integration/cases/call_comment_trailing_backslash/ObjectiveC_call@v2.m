#import <Foundation/Foundation.h>
#include <assert.h>
static int event_index = 0;
static void observe_event(long long actual) {
    const long long expected[] = {1, 1, 1, 2};
    assert(event_index < 4 && actual == expected[event_index]);
    event_index++;
}
static NSNumber *process(NSNumber *value) { observe_event(1); observe_event(value.longLongValue); return @(value.longLongValue + 100); }
static void verify_events(void) { assert(event_index == 4); }
int main(void) {
@autoreleasepool {
process(@1);  // trail \ .
process(@2);  // second
verify_events();
}
    return 0;
}
