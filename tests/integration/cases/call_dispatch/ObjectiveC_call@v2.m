#import <Foundation/Foundation.h>
static void store_item(id _a0, id _a1) { (void)_a0; (void)_a1; }
static void read_item(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
store_item(@1, @10);
read_item(@1);
}
    return 0;
}
