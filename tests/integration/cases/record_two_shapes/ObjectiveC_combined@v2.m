#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"metrics": @{@"count": @100, @"rate": @50},
    @"flags": @{@"retries": @3, @"timeout": @30},
};
(void)my_data;
my_data = @{
    @"metrics": @{@"count": @100, @"rate": @50},
    @"flags": @{@"retries": @3, @"timeout": @30},
};
    (void)my_data;
}
    return 0;
}
