use crate::gen::attributes::cocktributes::CockTribute;
use crate::gen::types::SchemaSkipType;

use rand::{Rng, prelude::SliceRandom, thread_rng};

use super::names;

/// Create a random set of attributes!
///
/// **Params**
/// - `generation: i32` The generation of the MonsterCock.
///
/// **Returns**
/// - `Vec<CockTribute>` The random attributes.
pub fn randomattributes(generation: u32) -> Vec<CockTribute> {
    // El generation
    let cock_gen = CockTribute::Generation { generation };
    // Create the schemas
    let mut schemas = Vec::new();
    for _ in 0..3 {
        // Create a random number between 0 and 4
        let rng = thread_rng().gen_range(0..6);
        schemas.push(rng);
    }
    let cock_schema = CockTribute::Schema {
        circles: schemas.contains(&1),
        squares: schemas.contains(&2),
        stripes: schemas.contains(&3),
        round_squares: schemas.contains(&4),
    };
    // Choose a gradient
    let gradient_choice = thread_rng().gen_range(0..3);
    let cock_gradient = CockTribute::Gradient {
        vertical: gradient_choice == 0,
        horizontal: gradient_choice == 1,
    };

    // Choose a Sunrise
    let num = thread_rng().gen_range(0..10);
    let cock_sunrise = if num > 7 {
        CockTribute::Sun {
            rising: true,
        }
    } else {
        CockTribute::Sun {
            rising: false,
        }
    };

    vec![cock_gen, cock_schema, cock_gradient, cock_sunrise]
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
    let places = vec![
      1, 2, 3, 5, 10
    ];
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
        thread_rng().gen_range(0..255)
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
    let types = vec![
        SchemaSkipType::Original,
        SchemaSkipType::V2
    ];
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