#import <Foundation/Foundation.h>
static void kHelper_list_stub_(id _a0) { (void)_a0; }
struct kHelperType_ { void (*list)(id); };
static const struct kHelperType_ kHelper = { .list = kHelper_list_stub_ };
int main(void) {
@autoreleasepool {
kHelper.list(@1);
}
    return 0;
}
