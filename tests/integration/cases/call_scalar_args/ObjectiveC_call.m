#import <Foundation/Foundation.h>
void process(id);
void check_(void) {
process(@"hello");
process(@(42));
process(@YES);
}
