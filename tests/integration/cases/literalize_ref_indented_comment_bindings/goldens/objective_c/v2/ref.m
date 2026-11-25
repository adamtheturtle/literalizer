#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
        id shared = @[
            @1,
            @2,
        ];
        id my_data = @[
            // A leading comment with { braces, "quotes", and // markers
            @"first\n{ \"quoted\" // text }",
            shared,
        ];
    (void)my_data;
}
    return 0;
}
