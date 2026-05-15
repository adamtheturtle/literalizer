#import <Foundation/Foundation.h>
static id process(id _a0) { (void)_a0; return nil; }
static void kTracer_emit_stub_(id _a0) { (void)_a0; }
struct kTracerType_ { void (*emit)(id); };
static const struct kTracerType_ kTracer = { .emit = kTracer_emit_stub_ };
int main(void) {
@autoreleasepool {
tracer.emit(process(@"hello"));
tracer.emit(process(@42));
tracer.emit(process(@YES));
}
    return 0;
}
