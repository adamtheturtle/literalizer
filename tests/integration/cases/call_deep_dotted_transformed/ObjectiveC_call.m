#import <Foundation/Foundation.h>
#pragma clang diagnostic ignored "-Wstrict-prototypes"
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
static id app_client_fetch_stub_() { return nil; }
struct clientType_ { id (*fetch)(); };
struct appType_ { struct clientType_ client; };
static const struct appType_ app = { .client = { .fetch = app_client_fetch_stub_ } };
#pragma clang diagnostic ignored "-Wstrict-prototypes"
#pragma clang diagnostic ignored "-Wdeprecated-non-prototype"
void emit();
void check_(void) {
emit(app.client.fetch(@"hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(@YES));
}
