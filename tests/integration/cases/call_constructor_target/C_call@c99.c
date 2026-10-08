#include <stdbool.h>
#include <stddef.h>
typedef struct CVal CVal;
typedef struct CKV CKV;
struct CVal {
    union {
        _Bool b;
        long long i;
        unsigned long long u;
        double f;
        const char *s;
        const CVal *a;
        const CKV *m;
    };
};
struct CKV { const char *k; CVal v; };
static void Playlist_new_stub_(CVal _a0) { (void)_a0; }
struct PlaylistType_ { void (*new)(CVal); };
static const struct PlaylistType_ Playlist = { .new = Playlist_new_stub_ };
int main(void) {
Playlist.new(((CVal){.i = 1}));
    return 0;
}
