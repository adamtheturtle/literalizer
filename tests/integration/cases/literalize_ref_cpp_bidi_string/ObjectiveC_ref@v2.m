#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id text = @((const char[]){'\141', '\342', '\200', '\252', '\142', '\000'});
id my_data = @{
    @"value": text,
};
    (void)my_data;
}
    return 0;
}
