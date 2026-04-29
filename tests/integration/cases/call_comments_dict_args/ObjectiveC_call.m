#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
// Test cases
process(@{@"type": @"create", @"pr_id": @"pr_1"});  // first case
process(@{@"type": @"update", @"pr_id": @"pr_2"});  // second case
// third case
process(@{@"type": @"delete", @"pr_id": @"pr_3"});
}
    return 0;
}
