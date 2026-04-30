typedef enum int {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
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
class ClientType_;
    task fetch(input _VVal payload); endtask
endclass
class AppType_;
    ClientType_ client = new();
endclass
AppType_ app = new();
initial begin
app.client.fetch(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"});
app.client.fetch(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""});
app.client.fetch(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
