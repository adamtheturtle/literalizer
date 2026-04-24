#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @{
    @"description": @"# not a comment\n",
    @"name": @"foo",
};
(void)my_data;
my_data = @{
    @"description": @"# not a comment\n",
    @"name": @"foo",
};
    (void)my_data;
}
