#import <Foundation/Foundation.h>
static id make_widget(id _a0) { (void)_a0; return nil; }
static void consume(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id my_data = make_widget(@42);
consume(my_data);
my_data = make_widget(@42);
consume(my_data);
}
    return 0;
}
