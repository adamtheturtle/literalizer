with A_Stub; use A_Stub;
procedure Main is
    procedure Op (Operation : A_Val) is begin null; end Op;
begin
    Op(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1")), AEntry ("draft", ABool (True))]);
    Op(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_2"))]);
end Main;
