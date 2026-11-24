#import <Foundation/Foundation.h>
static id make_widget(id _a0, id _a1) { (void)_a0, (void)_a1; return nil; }
static void consume(id _a0, id _a1) { (void)_a0, (void)_a1; }
int main(void) {
@autoreleasepool {
id my_data = make_widget(@42, @3);
consume(@3, my_data);
}
    return 0;
}
