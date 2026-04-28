#import <Foundation/Foundation.h>
int main(void) {
id my_data = @{
    @"name": @"Alice",
    @"scores": @[@10, @20, @30],
};
(void)my_data;
my_data = @{
    @"name": @"Alice",
    @"scores": @[@10, @20, @30],
};
    (void)my_data;
    return 0;
}
