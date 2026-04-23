#import <Foundation/Foundation.h>
static void m_Op_stub_(id _a0) { (void)_a0; }
struct mType_ { void (*Op)(id); };
static const struct mType_ m = { .Op = m_Op_stub_ };
void check_(void) {
m.Op(@{@"type": @"create", @"pr_id": @"pr_1", @"draft": @YES});
m.Op(@{@"type": @"create", @"pr_id": @"pr_2"});
}
