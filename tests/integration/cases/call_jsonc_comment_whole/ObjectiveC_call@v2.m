#import <Foundation/Foundation.h>
#include <assert.h>
static int *event_index(void) { static int index = 0; return &index; }
static void observe_event(long long actual) {
    const long long expected[] = {1, 42};
    assert(*event_index() < 2 && actual == expected[*event_index()]);
    ++*event_index();
}
static NSNumber *f(NSNumber *argument) { observe_event(1); observe_event(argument.longLongValue); return @(argument.longLongValue + 100); }
static void verify_events(void) { assert(*event_index() == 2); }
int main(void) {
@autoreleasepool {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(@42);
verify_events();
}
    return 0;
}
