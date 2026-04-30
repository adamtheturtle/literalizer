#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id my_var = @42;
id my_other = @7;
process(@[@{@"ref": @"my_var"}, @42, @"static"]);
process(@[@{@"ref": @"my_other"}, @7, @"label"]);
}
    return 0;
}
