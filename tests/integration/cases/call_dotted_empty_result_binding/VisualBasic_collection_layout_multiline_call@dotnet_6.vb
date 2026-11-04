Imports System.Collections.Generic
Module Check
    Class ThingType_0_
        Public Function go(value As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim thing As New ThingType_0_()
    Sub _calls()
        Dim my_data = thing.go(New Object() {})
    End Sub
End Module
