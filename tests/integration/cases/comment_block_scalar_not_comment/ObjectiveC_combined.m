#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @{
    @"description": @"# not a comment\n",
    @"name": @"foo",
};
my_data = @{
    @"description": @"# not a comment\n",
    @"name": @"foo",
};
    (void)my_data;
}
