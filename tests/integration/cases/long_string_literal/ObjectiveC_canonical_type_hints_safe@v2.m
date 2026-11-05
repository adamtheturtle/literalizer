#import <Foundation/Foundation.h>
int main(void) {
  @autoreleasepool {
    id my_data = @{
      @"long_str" :
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
          @"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      @"quoted" :
          @"a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\""
          @"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba"
          @"\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b"
          @"a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\""
          @"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba"
          @"\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b"
          @"a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\""
          @"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba"
          @"\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b"
          @"a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b",
      @"wide" :
          @"中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"
          @"中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"
          @"中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"
          @"中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"
          @"中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"
          @"中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"
          @"中中",
    };
    (void)my_data;
  }
  return 0;
}
