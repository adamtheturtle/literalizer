with A_Stub; use A_Stub;
procedure Main is
    type Throttler_T is tagged null record;
    function Check (Self : Throttler_T; User_Id : A_Val; Ts : A_Val) return A_Val is (ANull);
    Throttler : Throttler_T;
    procedure Emit (Arg : A_Val) is begin null; end Emit;
begin
    emit(throttler.check(user_id => "user_1", ts => 1000.0));
    emit(throttler.check(user_id => "user_2", ts => 2000.5));
end Main;
