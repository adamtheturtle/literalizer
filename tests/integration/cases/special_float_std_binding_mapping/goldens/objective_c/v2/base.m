#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id std = @{
    @"nan": @(NAN),
    @"positive": @(INFINITY),
    @"negative": @(-INFINITY),
};
    (void)std;
}
    return 0;
}
