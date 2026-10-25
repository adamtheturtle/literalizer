#import <Foundation/Foundation.h>
static void consume_widget(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id ref_data = @[
    @1,
    @2,
];
id my_data = @[
    @0,
];
consume_widget(my_data);
my_data = ref_data;
consume_widget(my_data);
}
    return 0;
}
