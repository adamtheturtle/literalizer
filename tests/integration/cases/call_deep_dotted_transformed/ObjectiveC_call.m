#import <Foundation/Foundation.h>
static id app_client_fetch_stub_(id _a0) { (void)_a0; return nil; }
struct clientType_ { id (*fetch)(id); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .fetch = app_client_fetch_stub_ } };
void emit(id);
void check_(void) {
emit(app.client.fetch(@"hello"));
emit(app.client.fetch(@(42)));
emit(app.client.fetch(@YES));
}
