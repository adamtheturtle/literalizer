#import <Foundation/Foundation.h>
static void kPlaylist_new_stub_(id _a0) { (void)_a0; }
struct kPlaylistType_ { void (*new)(id); };
static const struct kPlaylistType_ kPlaylist = { .new = kPlaylist_new_stub_ };
int main(void) {
@autoreleasepool {
kPlaylist.new(@1);
kPlaylist.new(@2);
}
    return 0;
}
