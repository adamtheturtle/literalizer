#import <Foundation/Foundation.h>
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
static id throttler_check_stub_() { return nil; }
struct throttlerType_ { id (*check)(); };
static const struct throttlerType_ throttler = { .check = throttler_check_stub_ };
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
void emit();
void check_(void) {
emit(throttler.check(@"user_1", 1000.0));
emit(throttler.check(@"user_2", 2000.5));
}
