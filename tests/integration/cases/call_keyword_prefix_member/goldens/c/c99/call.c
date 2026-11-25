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
static void Playlist_newValue_stub_(CVal _a0) { (void)_a0; }
struct PlaylistType_ { void (*newValue)(CVal); };
static const struct PlaylistType_ Playlist = { .newValue = Playlist_newValue_stub_ };
int main(void) {
Playlist.newValue(((CVal){.i = 1}));
    return 0;
}
