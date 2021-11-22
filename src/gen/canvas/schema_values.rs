use crate::gen::types::SchemaSkipType;

#[derive(Debug, Clone, PartialEq)]
pub struct SchemaValues {
    pub title: String,
    pub modulus: i32,
    pub size: i32,
    pub skips: Vec<i32>,
    pub skip_type: SchemaSkipType,
}

impl SchemaValues {
    pub fn new(
        title: String,
        modulus: i32,
        size: i32,
        skips: Vec<i32>,
        skip_type: SchemaSkipType,
    ) -> Self {
        Self {
            title,
            modulus,
            size,
            skips,
            skip_type,
        }
    }
}