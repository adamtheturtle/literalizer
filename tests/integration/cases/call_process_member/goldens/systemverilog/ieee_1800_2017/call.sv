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
class ProcessType_;
    task fetch(input _VVal data); endtask
endclass
class AppType_;
    ProcessType_ process = new();
endclass
AppType_ app = new();
initial begin
void'(app.process.fetch(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"data\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"hello\"}}}"}));
void'(app.process.fetch(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"data\", v: _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: \"\"}}}"}));
void'(app.process.fetch(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"data\", v: _VVal'{tag: _VVAL_BOOL, i: 1, r: 0.0, s: \"\"}}}"}));
end
endmodule
