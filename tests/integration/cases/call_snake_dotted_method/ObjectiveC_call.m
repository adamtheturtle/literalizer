#import <Foundation/Foundation.h>
static void kMy_App_http_client_fetch_stub_(id _a0) { (void)_a0; }
struct http_clientType_ { void (*fetch)(id); };
struct kMy_AppType_ { struct http_clientType_ http_client; };
static const struct kMy_AppType_ kMy_App = { .http_client = { .fetch = kMy_App_http_client_fetch_stub_ } };
int main(void) {
kMy_App.http_client.fetch(@"hello");
kMy_App.http_client.fetch(@42);
kMy_App.http_client.fetch(@YES);
    return 0;
}
