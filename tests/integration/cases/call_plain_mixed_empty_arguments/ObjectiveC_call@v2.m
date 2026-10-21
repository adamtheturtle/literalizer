#import <Foundation/Foundation.h>
static id make_widget(id _a0, id _a1, id _a2) { (void)_a0, (void)_a1, (void)_a2; return nil; }
int main(void) {
@autoreleasepool {
make_widget(@[], @[@1], @[]);
make_widget(@[@"text"], @[@2], @[]);
make_widget(@[], @[@"text"], @[]);
make_widget(@[@"text"], @[@2], @[@3]);
}
    return 0;
}
