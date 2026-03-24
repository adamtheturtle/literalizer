#import <Foundation/Foundation.h>
void _check(void) {
    id my_data = @{
    @"key": @"value \" # not a comment",  // real
};
    (void)my_data;
}
