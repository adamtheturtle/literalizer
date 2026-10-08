typedef enum int {_VVAL_BOOL, _VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
typedef struct {
    string k;
    _VVal v;
} _VKV;
module main;
class PlaylistType_;
    task new(input _VVal x); endtask
endclass
PlaylistType_ Playlist = new();
initial begin
Playlist.new(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
