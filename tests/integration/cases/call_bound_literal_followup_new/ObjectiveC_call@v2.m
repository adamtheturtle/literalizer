#import <Foundation/Foundation.h>
#include <assert.h>
static int *event_index(void) { static int index = 0; return &index; }
static void observe_event(long long actual) {
    const long long expected[] = {1, 42, 2, 142};
    assert(*event_index() < 4 && actual == expected[*event_index()]);
    ++*event_index();
}
static NSNumber *make_widget(NSNumber *argument) { observe_event(1); observe_event(argument.longLongValue); return @(argument.longLongValue + 100); }
static void consume(NSNumber *argument) { observe_event(2); observe_event(argument.longLongValue); }
static void verify_events(void) { assert(*event_index() == 4); }
int main(void) {
@autoreleasepool {
id my_data = make_widget(@42);
consume(my_data);
verify_events();
}
    return 0;
}
