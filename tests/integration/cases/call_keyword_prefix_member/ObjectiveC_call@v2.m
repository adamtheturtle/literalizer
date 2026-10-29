#import <Foundation/Foundation.h>
static void kPlaylist_newValue_stub_(id _a0) { (void)_a0; }
struct kPlaylistType_ { void (*newValue)(id); };
static const struct kPlaylistType_ kPlaylist = { .newValue = kPlaylist_newValue_stub_ };
int main(void) {
@autoreleasepool {
kPlaylist.newValue(@1);
}
    return 0;
}
