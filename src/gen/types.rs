#[derive(Clone, PartialEq, Debug)]
pub enum CockType {
    Default,
    Solana,
}

impl CockType {
    /// Create a new CockType with a given name.
    /// 
    /// # Arguments
    /// `string` The name of the CockType.
    /// 
    /// # Returns
    /// A new CockType with the given name.
    pub fn from_string(string: String) -> CockType {
        match string.to_lowercase().as_str() {
            "default" => CockType::Default,
            "solana" => CockType::Solana,
            "def" => CockType::Default,
            "sol" => CockType::Solana,
            "d" => CockType::Default,
            "s" => CockType::Solana,
            _ => panic!("Invalid CockType: {}", string),
        }
    }
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