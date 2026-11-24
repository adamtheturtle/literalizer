with A_Stub; use A_Stub;
procedure Main is
    function Check (User_Id : A_Val; Ts : A_Val) return A_Val is (ANull);
    procedure Emit (Arg : A_Val) is begin null; end Emit;
begin
    emit(Check(user_id => AStr ("user_1"), ts => AFloat (1000.0)));
    emit(Check(user_id => AStr ("user_2"), ts => AFloat (2000.5)));
end Main;
