#import <Foundation/Foundation.h>
static id make_widget(id _a0) { (void)_a0; return nil; }
static void consume(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id my_data = make_widget(@7);
consume(my_data);
my_data = make_widget(@13) ?
make_widget(@13) // inner
: nil; // trailing
consume(my_data);
}
    return 0;
}
