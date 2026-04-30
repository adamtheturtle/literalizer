#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id my_var = @42;
process(@{@"key": @{@"ref": @"my_var"}, @"count": @42});
}
    return 0;
}
