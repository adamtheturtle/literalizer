#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"user": @{@"id": @1, @"name": @"Alice"},
    @"project": @{@"title": @"report", @"tags": @[@"draft", @"urgent"]},
};
    (void)my_data;
}
    return 0;
}
