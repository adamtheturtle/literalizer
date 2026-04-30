#import <Foundation/Foundation.h>
static void process(id _a0, id _a1, id _a2) { (void)_a0; (void)_a1; (void)_a2; }
int main(void) {
@autoreleasepool {
process(@1, @0, @3600);  // Jan 1 1970 00:00:00 - 01:00:00
process(@5, @0, @3600);  // Jan 1 1970 00:00:05 - 01:00:05
process(@2, @0, @5400);  // Jan 1 1970 00:00:02 - 01:30:02
}
    return 0;
}
