#import <Foundation/Foundation.h>
static void app_mgr_op_stub_(id _a0) { (void)_a0; }
struct mgrType_ { void (*op)(id); };
struct appType_ { struct mgrType_ mgr; };
static const struct appType_ app = { .mgr = { .op = app_mgr_op_stub_ } };
void check_(void) {
app.mgr.op(@{@"type": @"create", @"pr_id": @"pr_1", @"draft": @YES});
app.mgr.op(@{@"type": @"create", @"pr_id": @"pr_2"});
}
