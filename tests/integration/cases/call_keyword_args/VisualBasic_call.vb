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
        emit(throttler.check("user_1", 1000.0))
        emit(throttler.check("user_2", 2000.5))
    End Sub
End Module
