#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
            id shared = @[
                @1,
                @2,
            ];
            id other = @3;
            id payload = @"\n    shared : Val\nshared = RInt 99";
            id my_data = @{
                @"a": shared,
                @"b": other,
                @"payload": payload,
            };
    (void)my_data;
}
    return 0;
}
