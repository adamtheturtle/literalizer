Imports System.Collections.Generic
Module Check
    Class ThingType_0_
        Public Function go(value As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim thing As New ThingType_0_()
    Sub _calls()
        Dim item = New Integer() {
            1,
            2
        }
        thing.go(item)
    End Sub
End Module
