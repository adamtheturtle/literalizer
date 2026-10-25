#import <Foundation/Foundation.h>
static void consume_widget(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id missing = @[
    @1,
    @2,
];
id my_data = missing;
consume_widget(my_data);
}
    return 0;
}
