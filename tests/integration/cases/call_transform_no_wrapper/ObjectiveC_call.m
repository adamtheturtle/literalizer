#import <Foundation/Foundation.h>
id process(id);
void check_(void) {
process(@"hello");
process(@(42));
process(@YES);
}
