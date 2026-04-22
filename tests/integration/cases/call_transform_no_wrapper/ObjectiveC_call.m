#import <Foundation/Foundation.h>
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
id process();
void check_(void) {
process(@"hello");
process(42);
process(@YES);
}
