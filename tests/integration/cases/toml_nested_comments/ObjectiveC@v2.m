#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    // About the first dotted key.
    // About the second dotted key.
    @"dotted": @{@"first": @1, @"second": @2},
    @"plain": @3,  // About the plain key.
    // Inside the table.
    @"table": @{@"inner": @4},
    // Before the first entry.
    // Before the second entry.
    @"entries": @[@{@"name": @"one"}, @{@"name": @"two"}],
};
    (void)my_data;
}
    return 0;
}
