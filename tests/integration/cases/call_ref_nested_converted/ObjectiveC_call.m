#import <Foundation/Foundation.h>
static void process(id _a0) { (void)_a0; }
int main(void) {
@autoreleasepool {
id myVar = @42;
process(@[@{@"ref": @"myVar"}, @42, @"static"]);
}
    return 0;
}
