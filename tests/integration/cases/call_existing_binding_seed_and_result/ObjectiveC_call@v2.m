#import <Foundation/Foundation.h>
static id make_widget(id _a0) { (void)_a0; return nil; }
static void consume_widget(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id my_data = make_widget(@0);
consume_widget(my_data);
my_data = make_widget(@1);
consume_widget(my_data);
}
    return 0;
}
