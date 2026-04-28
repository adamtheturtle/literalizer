#import <Foundation/Foundation.h>
static id kApp_client_fetch_stub_(id _a0) { (void)_a0; return nil; }
struct clientType_ { id (*fetch)(id); };
struct kAppType_ { struct clientType_ client; };
static const struct kAppType_ kApp = { .client = { .fetch = kApp_client_fetch_stub_ } };
static void emit(id _a0) { (void)_a0; }
int main(void) {
emit(kApp.client.fetch(@"hello"));
emit(kApp.client.fetch(@42));
emit(kApp.client.fetch(@YES));
    return 0;
}
