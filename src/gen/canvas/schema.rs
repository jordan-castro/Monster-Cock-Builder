use crate::{
    gen::types::SchemaSkipType,
    learning::interface::make_schema, utils::randomify::{random_skip_values, random_skip_type},
};
use itertools::Itertools;
use rand::Rng;

#[derive(Clone, PartialEq)]
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
        let mut schema = Schema {
            title,
            modulus,
            size,
            skips,
            skip_type,
        };
        match schema.skip_type {
            SchemaSkipType::Original => {}
            SchemaSkipType::V2 => {
                schema.size = schema.modulus;
            }
        }

        schema
    }

    /// Generates a random (valid) schema based on the title.
    pub fn get_valid_schema(title: String) -> Self {
        // Interact with the Model
        make_schema(title)
    }

    pub fn stringify_skips(&self) -> String {
        self.skips.iter().join(",")
    }

    pub fn random_schema(title: String) -> Self {
        let modulus = get_modulus();
        let size = get_draw_size();
        Self::new(
            title,
            modulus,
            size,
            random_skip_values(),
            random_skip_type(),
        )
    }

    /// Print to the screen the values of the draw.
    pub fn debug(&self) {
        println!("===============================");
        println!("{}", self.title);
        println!("Modulus: {}", self.modulus);
        if self.size == 0 {
            println!("Size: random");
        } else {
            println!("Size: {}", self.size);
        }
        println!("Skip values: {}", self.stringify_skips());
        println!("Skip type: {}", self.skip_type.to_string());
    }
}

fn get_modulus() -> i32 {
    rand::thread_rng().gen_range(2..30)
}

fn get_draw_size() -> i32 {
    rand::thread_rng().gen_range(1..100)
}