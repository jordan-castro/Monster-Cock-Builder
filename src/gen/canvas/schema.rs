use crate::{gen::types::SchemaSkipType, utils::randomify::random_skip_values};
use itertools::Itertools;
use rand::Rng;

#[derive(Debug, Clone, PartialEq)]
pub struct Schema {
    pub title: String,
    pub modulus: i32,
    pub size: i32,
    pub skips: Vec<i32>,
    pub skip_type: SchemaSkipType,
}

impl Schema {
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

    pub fn stringify_skips(&self) -> String {
        self.skips.iter().join(",")
    }

    pub fn random_schema(title: String) -> Self {
        let modulus = get_modulus();
        let size = get_draw_size(modulus);
        Schema {
            title,
            modulus,
            size,
            skips: random_skip_values(),
            skip_type: SchemaSkipType::Original,
        }
    }
}

///
/// Get a random Modulus from certain possible values.
///
/// # Returns
/// `i32` The random modulus.
///
fn get_modulus() -> i32 {
    rand::thread_rng().gen_range(2..30)
}

///
/// Get a size for the draw object.
///
/// # Returns
/// `i32` The size of the draw.
///
fn get_draw_size(modulus: i32) -> i32 {
    rand::thread_rng().gen_range(1..modulus + 20)
}
