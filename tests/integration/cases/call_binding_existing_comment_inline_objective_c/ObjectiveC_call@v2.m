#import <Foundation/Foundation.h>
static id make_widget(id _a0) { (void)_a0; return nil; }
int main(void) {
@autoreleasepool {
id my_data = make_widget(@42);
make_widget(my_data);
my_data = make_widget(my_data); // note
make_widget(my_data);
}
    return 0;
}
