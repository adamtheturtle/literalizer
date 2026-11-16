#import <Foundation/Foundation.h>
#include <assert.h>
static int event_index = 0;
static void observe_event(long long actual) {
    const long long expected[] = {1, 1};
    assert(event_index < 2 && actual == expected[event_index]);
    event_index++;
}
static NSNumber *capture(NSNumber *__proto__) { observe_event(1); observe_event(__proto__.longLongValue); return @(__proto__.longLongValue + 100); }
static void verify_events(void) { assert(event_index == 2); }
int main(void) {
@autoreleasepool {
capture(@1);
verify_events();
}
    return 0;
}
