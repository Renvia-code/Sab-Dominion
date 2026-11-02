// Query FCT_RELIABILITY (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "fct_reliability.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Renamed = Table.RenameColumns(UpperNames, {{"CUSTOMERS", "Customers Served"}}),
    Selected = Table.SelectColumns(Renamed, {"UTILITY_KEY", "UTILITY_ID", "STATE", "YEAR", "STANDARD", "SOURCE", "Customers Served", "SAIDI_ALL", "SAIFI_ALL", "CAIDI_ALL", "SAIDI_EX_MED", "SAIFI_EX_MED", "CAIDI_EX_MED", "STORM_SAIDI", "STORM_SAIFI", "CUST_MINUTES_ALL", "CUST_MINUTES_EX_MED", "CUST_INTERRUPTIONS_ALL", "CUST_INTERRUPTIONS_EX_MED", "MAX_KV", "AUTO_RECORDED", "MOMENTARY_DEF", "INACTIVE_INCLUDED"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"UTILITY_KEY", type text}, {"UTILITY_ID", type number}, {"STATE", type text}, {"YEAR", type number}, {"STANDARD", type text}, {"SOURCE", type text}, {"Customers Served", type number}, {"SAIDI_ALL", type number}, {"SAIFI_ALL", type number}, {"CAIDI_ALL", type number}, {"SAIDI_EX_MED", type number}, {"SAIFI_EX_MED", type number}, {"CAIDI_EX_MED", type number}, {"STORM_SAIDI", type number}, {"STORM_SAIFI", type number}, {"CUST_MINUTES_ALL", type number}, {"CUST_MINUTES_EX_MED", type number}, {"CUST_INTERRUPTIONS_ALL", type number}, {"CUST_INTERRUPTIONS_EX_MED", type number}, {"MAX_KV", type number}, {"AUTO_RECORDED", type logical}, {"MOMENTARY_DEF", type text}, {"INACTIVE_INCLUDED", type logical}}, "en-US")
in
    Typed
