#import <Foundation/Foundation.h>
static void mgr_Op_stub_(id _a0) { (void)_a0; }
struct mgrType_ { void (*Op)(id); };
static const struct mgrType_ mgr = { .Op = mgr_Op_stub_ };
void check_(void) {
mgr.Op(@{@"type": @"create", @"pr_id": @"pr_1", @"draft": @YES});
mgr.Op(@{@"type": @"create", @"pr_id": @"pr_2"});
}
