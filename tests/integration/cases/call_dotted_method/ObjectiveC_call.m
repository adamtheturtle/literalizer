#import <Foundation/Foundation.h>
static void app_client_fetch_stub_(id _a0) { (void)_a0; }
struct clientType_ { void (*fetch)(id); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .fetch = app_client_fetch_stub_ } };
void check_(void) {
app.client.fetch(@"hello");
app.client.fetch(@(42));
app.client.fetch(@YES);
}
