#import <Foundation/Foundation.h>
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
static void app_client_fetch_stub_() {}
struct clientType_ { void (*fetch)(); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .fetch = app_client_fetch_stub_ } };
void check_(void) {
app.client.fetch(@"hello");
app.client.fetch(42);
app.client.fetch(@YES);
}
