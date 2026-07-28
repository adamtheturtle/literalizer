#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id my_list = @[];
process(@[@[@{@"inner": my_list}]]);
}
    return 0;
}
