#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
void check_(void) {
process(@"hello");
process(@(42));
process(@YES);
}
