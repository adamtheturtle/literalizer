#import <Foundation/Foundation.h>
static void process(void) {}
int main(void) {
@autoreleasepool {
process();
process();
}
    return 0;
}
