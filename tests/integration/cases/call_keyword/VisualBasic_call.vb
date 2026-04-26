Imports System.Collections.Generic
Module Check
    Class ThrottlerType_0_
        Public Function check(user_id As Object, ts As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim throttler As New ThrottlerType_0_()
    Function emit(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(throttler.check(user_id:="user_1", ts:=1000.0))
        emit(throttler.check(user_id:="user_2", ts:=2000.5))
    End Sub
End Module
