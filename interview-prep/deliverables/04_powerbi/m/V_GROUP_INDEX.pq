// Query V_GROUP_INDEX (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "v_group_index.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"PEER_GROUP", "YEAR", "UTILITIES", "CUSTOMERS", "SAIFI_EX_MED", "SAIDI_EX_MED", "CAIDI_EX_MED"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"PEER_GROUP", type text}, {"YEAR", type number}, {"UTILITIES", type number}, {"CUSTOMERS", type number}, {"SAIFI_EX_MED", type number}, {"SAIDI_EX_MED", type number}, {"CAIDI_EX_MED", type number}}, "en-US")
in
    Typed
