#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @{
    @"level1": @{@"level2": @{@"level3": @{@"level4": @{@"value": @"deep", @"items": @[@"a", @"b"]}}, @"sibling": @(42)}, @"tags": @[@{@"name": @"tag1", @"meta": @{@"priority": @(1), @"labels": @[@"x", @"y"]}}]},
};
    (void)_v;
}
