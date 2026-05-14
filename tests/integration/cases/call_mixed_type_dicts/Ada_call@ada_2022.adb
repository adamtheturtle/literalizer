with A_Stub; use A_Stub;
procedure Main is
    procedure Run (Operation : A_Val) is begin null; end Run;
begin
    Run(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1")), AEntry ("draft", ABool (True))]);
    Run(operation => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_2"))]);
end Main;
