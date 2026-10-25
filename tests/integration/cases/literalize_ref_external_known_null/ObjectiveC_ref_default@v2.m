#import <Foundation/Foundation.h>
static void consume_widget(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id item = [NSNull null];
id my_data = [NSNull null];
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
}
    return 0;
}
