#import <Foundation/Foundation.h>
int main(void) {
id my_data = @{
    @"1": @"one",
    @"2": @"two",
    @"42": @"answer",
};
(void)my_data;
my_data = @{
    @"1": @"one",
    @"2": @"two",
    @"42": @"answer",
};
    (void)my_data;
    return 0;
}
