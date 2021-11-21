#[derive(Clone, PartialEq, Debug)]
pub enum CockType {
    Default,
    Solana,
}

#[derive(Clone, PartialEq, Debug)]
pub enum SchemaSkipType {
    Original,
    V2,
}

impl SchemaSkipType {
    pub fn to_string(&self) -> String {
        let as_str= match self {
            SchemaSkipType::Original => "original",
            SchemaSkipType::V2 => "v2",
        };
        as_str.to_string()
    }
}