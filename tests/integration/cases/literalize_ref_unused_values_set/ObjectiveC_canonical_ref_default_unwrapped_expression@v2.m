#import <Foundation/Foundation.h>
static void consume_widget(id _a0) {
  (void)_a0;
}
int main(void) {
  @autoreleasepool {
    consume_widget([NSSet setWithArray:@[
      @1,
      @2,
    ]]);
  }
  return 0;
}
