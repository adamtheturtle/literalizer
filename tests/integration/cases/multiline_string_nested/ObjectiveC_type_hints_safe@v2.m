#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"outer": @[@[@"nested first line\n  indented\n\nnested last line\n"]],
};
    (void)my_data;
}
    return 0;
}
