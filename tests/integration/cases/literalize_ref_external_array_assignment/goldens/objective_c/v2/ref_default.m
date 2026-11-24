#import <Foundation/Foundation.h>
static void consume_widget(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id shared = @[
    @1,
    @2,
];
id my_data = @[
    @0,
];
consume_widget(my_data);
my_data = shared;
consume_widget(my_data);
}
    return 0;
}
