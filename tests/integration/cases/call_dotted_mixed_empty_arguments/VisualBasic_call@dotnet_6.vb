Imports System.Collections.Generic
Module Check
    Class ThingType_0_
        Public Function go(before As Object, populated As Object, after As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim thing As New ThingType_0_()
    Sub _calls()
        thing.go(New Object() {}, New Integer() {1}, New Object() {})
        thing.go(New String() {"text"}, New Integer() {2}, New Object() {})
        thing.go(New Object() {}, New String() {"text"}, New Object() {})
        thing.go(New String() {"text"}, New Integer() {2}, New Integer() {3})
    End Sub
End Module
