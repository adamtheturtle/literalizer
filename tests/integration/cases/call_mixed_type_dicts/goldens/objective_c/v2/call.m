#import <Foundation/Foundation.h>
static void kApp_mgr_run_stub_(id _a0) { (void)_a0; }
struct mgrType_ { void (*run)(id); };
struct kAppType_ { struct mgrType_ mgr; };
static const struct kAppType_ kApp = { .mgr = { .run = kApp_mgr_run_stub_ } };
int main(void) {
@autoreleasepool {
kApp.mgr.run(@{@"type": @"create", @"pr_id": @"pr_1", @"draft": @YES});
kApp.mgr.run(@{@"type": @"create", @"pr_id": @"pr_2"});
}
    return 0;
}
