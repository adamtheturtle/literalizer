#import <Foundation/Foundation.h>
static void check_(void) {
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
