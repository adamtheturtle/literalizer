#import <Foundation/Foundation.h>
int main(void) {
id my_data = @{
    @"level1": @{@"level2": @{@"level3": @{@"level4": @{@"value": @"deep", @"items": @[@"a", @"b"]}}, @"sibling": @42}, @"tags": @[@{@"name": @"tag1", @"meta": @{@"priority": @1, @"labels": @[@"x", @"y"]}}]},
};
(void)my_data;
my_data = @{
    @"level1": @{@"level2": @{@"level3": @{@"level4": @{@"value": @"deep", @"items": @[@"a", @"b"]}}, @"sibling": @42}, @"tags": @[@{@"name": @"tag1", @"meta": @{@"priority": @1, @"labels": @[@"x", @"y"]}}]},
};
    (void)my_data;
    return 0;
}
