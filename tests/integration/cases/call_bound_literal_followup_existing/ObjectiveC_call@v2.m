#import <Foundation/Foundation.h>
#include <assert.h>
static int event_index = 0;
static void observe_event(long long actual) {
    const long long expected[] = {2, 42, 1, 42, 2, 142};
    assert(event_index < 6 && actual == expected[event_index]);
    event_index++;
}
static NSNumber *make_widget(NSNumber *value) { observe_event(1); observe_event(value.longLongValue); return @(value.longLongValue + 100); }
static void consume(NSNumber *value) { observe_event(2); observe_event(value.longLongValue); }
static void verify_events(void) { assert(event_index == 6); }
int main(void) {
@autoreleasepool {
id my_data = @42;
consume(my_data);
my_data = make_widget(@42);
consume(my_data);
verify_events();
}
    return 0;
}
