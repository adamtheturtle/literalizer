Imports System.Collections.Generic
Module Check
    Class ThrottlerType_0_
        Public Function check() As Object
            Return Nothing
        End Function
    End Class
    Dim throttler As New ThrottlerType_0_()
    Sub _calls()
        throttler.check()
        throttler.check()
    End Sub
End Module
