#import <Foundation/Foundation.h>
int main(void) {
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
    return 0;
}
