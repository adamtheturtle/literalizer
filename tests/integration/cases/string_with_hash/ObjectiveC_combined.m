#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @"issue #{42}",
    @"color #red",
];
(void)my_data;
my_data = @[
    @"issue #{42}",
    @"color #red",
];
    (void)my_data;
}
