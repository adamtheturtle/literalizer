#import <Foundation/Foundation.h>
static id throttler_check_stub_(id _a0, id _a1) { (void)_a0; (void)_a1; return nil; }
struct throttlerType_ { id (*check)(id, id); };
static const struct throttlerType_ throttler = { .check = throttler_check_stub_ };
static void emit(id _a0) { (void)_a0; }
void check_(void) {
emit(throttler.check(@"user_1", @(1000.0)));
emit(throttler.check(@"user_2", @(2000.5)));
}
