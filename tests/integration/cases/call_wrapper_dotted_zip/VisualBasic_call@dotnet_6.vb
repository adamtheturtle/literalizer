Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Class HelpersType_0_
        Public Function emit(_call As Object, _zip As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim helpers As New HelpersType_0_()
    Sub _calls()
        helpers.emit(process(1), 42)
    End Sub
End Module
