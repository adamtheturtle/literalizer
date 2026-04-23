#import <Foundation/Foundation.h>
void process(id, id);
void check_(void) {
id my_var = @[
    @(1),
    @(2),
    @(3),
];
id my_other = @[
    @(4),
    @(5),
    @(6),
];
process(my_var, @(42));
process(my_other, @(7));
}
