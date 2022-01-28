use crate::gen::attributes::cocktributes::CockTribute;
use crate::gen::types::SchemaSkipType;

use rand::{prelude::SliceRandom, thread_rng, Rng};

use super::names;

/// Create a random set of attributes!
///
/// **Params**
/// - `generation: i32` The generation of the MonsterCock.
///
/// **Returns**
/// - `Vec<CockTribute>` The random attributes.
pub fn randomattributes(generation: u32) -> Vec<CockTribute> {
    let mut attributes: Vec<CockTribute> = Vec::new();

    // El generation
    let cock_gen = CockTribute::Generation { generation };
    attributes.push(cock_gen);
    let mut has_schema = false;
    // Schema
    {
        let schema = rand::thread_rng().gen_range(0..7);
        let cock_schema = match schema {
            0 => Some(CockTribute::SchemaCircles),
            1 => Some(CockTribute::SchemaSquares),
            2 => Some(CockTribute::SchemaStripes),
            // 3 => CockTribute::SchemaRoundSquares,
            4 => Some(CockTribute::SchemaSpace),
            5 => Some(CockTribute::SchemaGSquares),
            _ => None,
        };
        if cock_schema.is_some() {
            attributes.push(cock_schema.unwrap());
            has_schema = true;
        }
    }
    // Gradient
    {
        let has_gradient = rand::thread_rng().gen_bool(0.5) && !has_schema;
        if has_gradient {
            let vertical = rand::thread_rng().gen_bool(0.5);
            let gradient = if vertical {
                CockTribute::GradientVertical
            } else {
                CockTribute::GradientHorizontal
            };
            attributes.push(gradient);
        }
    }
    // Sunrise direction
    {
        let mirrored = rand::thread_rng().gen_bool(0.5);
        if mirrored {
            attributes.push(CockTribute::SunRiseEast);
        } else {
            attributes.push(CockTribute::SunRiseWest);
        }
    }
    // Return the attributes
    attributes
}

/// Create a random Vector of values to use in the skip_draw method.
///
/// # Returns
/// - `Vec<i32>` The random values.
pub fn random_skip_values() -> Vec<i32> {
    // The random values to skip
    let mut skip_values: Vec<i32> = Vec::new();
    // The amount of values to skip
    let amount = rand::thread_rng().gen_range(1..10);
    // The place
    let places = vec![1, 2, 3, 5, 10];
    let place = places.choose(&mut rand::thread_rng()).unwrap();

    for x in 1..amount {
        skip_values.push(place * x);
    }

    if skip_values.is_empty() {
        vec![2, 3, 4, 5, 6, 7, 8]
    } else {
        skip_values
    }
}

/// A random RGB color
///
/// # Returns
/// - `(i32, i32, i32)` The random RGB color.
pub fn randomify_color() -> (i32, i32, i32) {
    (
        thread_rng().gen_range(0..255),
        thread_rng().gen_range(0..255),
        thread_rng().gen_range(0..255),
    )
}

/// Return a random value from a Vector of any type.
///
/// # Params
/// - `values: Vec<T>` The Vector of values to choose from.
///
/// # Returns
/// - `T` The random value.
pub fn random_value<T>(values: &Vec<T>) -> &T {
    // Get random value from the vector
    let random_value = values.choose(&mut rand::thread_rng()).unwrap();
    random_value
}

/// Get a random skip type.
pub fn random_skip_type() -> SchemaSkipType {
    let types = vec![SchemaSkipType::Original, SchemaSkipType::V2];
    random_value(&types).to_owned()
}

/// Find a random name
///
/// # Returns
/// - `String` The random name.
pub fn random_name(is_test_net: bool) -> String {
    let names = names::get_names(is_test_net);
    random_value(&names).to_owned()
}
