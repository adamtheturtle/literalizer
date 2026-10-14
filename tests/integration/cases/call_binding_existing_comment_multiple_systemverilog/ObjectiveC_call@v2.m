#import <Foundation/Foundation.h>
static id make_widget(id _a0) { (void)_a0; return nil; }
int main(void) {
@autoreleasepool {
id my_data = make_widget(@42);
my_data = make_widget(@42); // note
// extra
}
    return 0;
}
