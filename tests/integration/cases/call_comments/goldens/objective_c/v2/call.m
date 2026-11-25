#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
// Test cases
process(@"hello");  // single word
process(@"hello world");  // two words
// trailing comment
}
    return 0;
}
