with A_Stub; use A_Stub;
procedure Main is
    type Mgr_T is tagged null record;
    procedure Op (Self : in out Mgr_T; Operation : A_Val) is begin null; end Op;
    type App_T is tagged record Mgr : Mgr_T; end record;
    App : App_T;
begin
    app.mgr.op(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1")), AEntry ("draft", ABool (True))]);
    app.mgr.op(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_2"))]);
end Main;
