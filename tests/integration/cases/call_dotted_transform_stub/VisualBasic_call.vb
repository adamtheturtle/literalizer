Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Class TracerType_0_
        Public Function emit(_arg As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim tracer As New TracerType_0_()
    Sub _calls()
        tracer.emit(process("hello"))
        tracer.emit(process(42))
        tracer.emit(process(True))
    End Sub
End Module
