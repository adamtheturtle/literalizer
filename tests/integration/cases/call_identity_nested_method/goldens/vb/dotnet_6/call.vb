Imports System.Collections.Generic
Module Check
    Class ThingType_1_
        Public Function go() As Object
            Return Nothing
        End Function
    End Class
    Class OuterType_0_
        Public thing As New ThingType_1_()
    End Class
    Dim outer As New OuterType_0_()
    Sub _calls()
        outer.thing.go()
    End Sub
End Module
