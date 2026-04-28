#import <Foundation/Foundation.h>
static void kApp_mgr_op_stub_(id _a0) { (void)_a0; }
struct mgrType_ { void (*op)(id); };
struct kAppType_ { struct mgrType_ mgr; };
static const struct kAppType_ kApp = { .mgr = { .op = kApp_mgr_op_stub_ } };
int main(void) {
kApp.mgr.op(@{@"type": @"create", @"pr_id": @"pr_1", @"draft": @YES});
kApp.mgr.op(@{@"type": @"create", @"pr_id": @"pr_2"});
    return 0;
}
