#import <Foundation/Foundation.h>
static id kObj_ZVal_stub_(id _a0) { (void)_a0; return nil; }
struct kObjType_ { id (*ZVal)(id); };
static const struct kObjType_ kObj = { .ZVal = kObj_ZVal_stub_ };
int main(void) {
@autoreleasepool {
id my_data = kObj.ZVal(@42); // note
    (void)my_data;
}
    return 0;
}
