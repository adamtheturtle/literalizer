#import <Foundation/Foundation.h>
static void kApi_worker_process_stub_(id _a0, id _a1) { (void)_a0, (void)_a1; }
struct workerType_ { void (*process)(id, id); };
struct kApiType_ { struct workerType_ worker; };
static const struct kApiType_ kApi = { .worker = { .process = kApi_worker_process_stub_ } };
int main(void) {
@autoreleasepool {
kApi.worker.process(@[@1, @{}], @42);
kApi.worker.process(@[@2, @{@"x": @"s"}], @43);
}
    return 0;
}
