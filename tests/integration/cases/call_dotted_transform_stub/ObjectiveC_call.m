#import <Foundation/Foundation.h>
static id process(id _a0) { (void)_a0; return nil; }
static void kLog_emit_stub_(id _a0) { (void)_a0; }
struct kLogType_ { void (*emit)(id); };
static const struct kLogType_ kLog = { .emit = kLog_emit_stub_ };
int main(void) {
@autoreleasepool {
log.emit(process(@"hello"));
log.emit(process(@42));
log.emit(process(@YES));
}
    return 0;
}
