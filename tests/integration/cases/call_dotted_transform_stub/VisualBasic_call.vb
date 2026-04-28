Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Class LogType_0_
        Public Function emit(_arg As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim log As New LogType_0_()
    Sub _calls()
        log.emit(process("hello"))
        log.emit(process(42))
        log.emit(process(True))
    End Sub
End Module
