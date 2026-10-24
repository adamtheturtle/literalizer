#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    // A JSONC input case with both comment forms.
    @"url": @"https://example.org/a/*b*/",  // detail
    // continued
    @"count": @02,  // trailing line comment
};
    (void)my_data;
}
    return 0;
}
