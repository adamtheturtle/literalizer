with A_Stub; use A_Stub;
procedure Main is
    type MgrType_ is tagged null record;
    procedure Op (Self : in out MgrType_; Operation : A_Val) is begin null; end Op;
    type AppType_ is tagged record Mgr : MgrType_; end record;
    App : AppType_;
begin
    app.mgr.op(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1")), AEntry ("draft", ABool (True))]);
    app.mgr.op(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_2"))]);
end Main;
