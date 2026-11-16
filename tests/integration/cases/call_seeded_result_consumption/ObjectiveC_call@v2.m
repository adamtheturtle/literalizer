#import <Foundation/Foundation.h>
#include <assert.h>
static int event_index = 0;
static void observe_event(long long actual) {
    const long long expected[] = {2, 0, 1, 1, 2, 101};
    assert(event_index < 6 && actual == expected[event_index]);
    event_index++;
}
static NSNumber *make_widget(NSNumber *count) { observe_event(1); observe_event(count.longLongValue); return @(count.longLongValue + 100); }
static void consume_widget(NSNumber *count) { observe_event(2); observe_event(count.longLongValue); }
static void verify_events(void) { assert(event_index == 6); }
int main(void) {
@autoreleasepool {
id my_data = @0;
consume_widget(my_data);
my_data = make_widget(@1);
consume_widget(my_data);
verify_events();
}
    return 0;
}
