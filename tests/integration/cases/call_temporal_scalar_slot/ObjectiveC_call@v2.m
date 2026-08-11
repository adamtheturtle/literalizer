#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
process(@"09:30:00");
process([NSDate dateWithTimeIntervalSince1970:1705276800]);
process(@1);
}
    return 0;
}
