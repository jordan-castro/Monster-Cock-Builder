use std::collections::HashSet;

use crate::gen::colors::Color;
use serde_json::{json, Map, Value};

/// The Attributes for a MosterCock
#[derive(Clone, PartialEq, Debug)]
pub enum CockTribute {
    Generation {
        generation: u32,
    },
    Sun {
        rising: bool,
    },
    Gradient {
        vertical: bool,
        horizontal: bool,
    },
    Schema {
        circles: bool,
        squares: bool,
        stripes: bool,
        round_squares: bool,
    },
}

impl CockTribute {
    /// Create cock attributes from json. Used when loading a MonsterCock from
    /// a json file.
    ///
    /// # Arguments
    /// `attributes` The attributes in JSON format.
    ///
    /// # Returns
    /// A Vector of CockTributes
    pub fn from_json(attributes: Map<String, Value>) -> Vec<Self> {
        let mut cocktributes = Vec::new();
        let mut schemas: Vec<i32> = Vec::new();

        for attribute in attributes {
            // Convert the String to lower case
            let attribute_name = attribute.0.to_lowercase();
            // Check the value
            match attribute_name.as_str() {
                "generation" => {
                    let generation = attribute.1.as_u64().unwrap() as u32;
                    cocktributes.push(CockTribute::Generation { generation });
                }
                "sunrise" => {
                    let sunrise = attribute.1.as_bool().unwrap();
                    cocktributes.push(CockTribute::Sun { rising: sunrise });
                }
                "gradient" => {
                    let vertical = if attribute.1.as_str().unwrap().to_lowercase() == "vertical" {
                        true
                    } else {
                        false
                    };
                    cocktributes.push(CockTribute::Gradient {
                        vertical,
                        horizontal: !vertical,
                    });
                }
                "schema" => {
                    let schema = attribute.1.as_str().unwrap().to_lowercase();
                    if schema == "circles" {
                        schemas.push(0);
                    } else if schema == "squares" {
                        schemas.push(1);
                    } else if schema == "stripes" {
                        schemas.push(2);
                    } else if schema == "round_squares" {
                        schemas.push(3);
                    }
                }
                _ => {} // Do nothing by default
            };
        }
        // Check if we have any schemas
        if schemas.len() > 0 {
            let schema_attribute = CockTribute::Schema {
                circles: schemas.contains(&0),
                squares: schemas.contains(&1),
                stripes: schemas.contains(&2),
                round_squares: schemas.contains(&3),
            };
            cocktributes.push(schema_attribute);
        }
        cocktributes
    }
}

/// Convert a Contribute to a Vectore holding the Attribute base and the Attribute value.
///  
/// **Params:**
/// - `cocktribute: CockTribute` - The Cocktribute to convert.
///
/// **Returns:**
/// - `Vec<Vec<String>>` - The Attribute base and the Attribute value.
fn readable_cocktribute(cocktribute: CockTribute) -> Vec<Vec<String>> {
    let mut base = Vec::new();

    match cocktribute {
        CockTribute::Generation { generation } => {
            base.push(String::from("Generation"));
            base.push(generation.to_string());
            vec![base]
        }
        CockTribute::Sun { rising } => {
            base.push(String::from("Sunrise")); // Todo Change the name??
            base.push(if rising {
                String::from("East")
            } else {
                String::from("West")
            });
            vec![base]
        }
        CockTribute::Gradient {
            vertical,
            horizontal,
        } => {
            base.push(String::from("Gradient"));
            if vertical {
                base.push(String::from("Vertical"));
            } else if horizontal {
                base.push(String::from("Horizontal"));
            } else {
                base.push(String::from("None"));
            }
            vec![base]
        }
        CockTribute::Schema {
            circles,
            squares,
            stripes,
            round_squares,
        } => {
            let mut result = Vec::new();
            if circles {
                result.push(vec![String::from("Schema"), String::from("Circles")]);
            }
            if squares {
                result.push(vec![String::from("Schema"), String::from("Squares")]);
            }
            if stripes {
                result.push(vec![String::from("Schema"), String::from("Stripes")]);
            }
            if round_squares {
                result.push(vec![String::from("Schema"), String::from("Round Squares")]);
            }
            result
        }
    }
}

/// Create a JSON string object for the CockTributes for the monstercock.
///
/// **Params**
/// - `cocktributes: Vec<CockTribute>` The CockTributes to convert.
/// - `colors: Vec<Colors>` The list of colors used on the MonsterCock.
///
/// **Returns:**
/// - `Value` - The JSON.
pub fn attributes_json(colors: Vec<Color>, cocktributes: Vec<CockTribute>) -> Value {
    let mut attributes = Vec::new();

    // Grab the colors based on the value of a certain color
    let grab_colors = |value: &str| {
        let inner = colors.clone();
        // Grab the colors where the .attribute_title is equal to the value
        let colors_of_value = inner
            .into_iter()
            .filter(|color| color.attribute_title.as_str() == value)
            .collect::<Vec<Color>>();
        // Return the names of the colors_of_Value
        colors_of_value
            .into_iter()
            .map(|color| color.name.clone())
            .collect::<Vec<String>>()
    };

    // Crea los attributes desde los colores
    let create_attribute_from_color_names = |color_names: Vec<String>| {
        // Remove repeated colors
        let color_names = color_names.into_iter().collect::<HashSet<_>>();
        // Join the colors with a -
        let color_names: Vec<String> = color_names.into_iter().collect();
        color_names.join("-")
    };

    // Create the json for an attribute
    let attribute_json = |tra: &str, value: _| {
        json!({
            "trait_type": tra,
            "value": value
        })
    };

    // Toma los colores
    let comb_colors = grab_colors("Comb");
    let beak_colors = grab_colors("Beak");
    let eye_colors = grab_colors("Eye");
    let neck_colors = grab_colors("Neck");
    let back_colors = grab_colors("Back");
    let chest_colors = grab_colors("Chest");
    let wing_colors = grab_colors("Wing");
    let leg_colors = grab_colors("Leg");

    // Put the attributes in attributes json
    attributes.insert(
        0,
        attribute_json("Comb", create_attribute_from_color_names(comb_colors)),
    );
    attributes.insert(
        1,
        attribute_json("Beak", create_attribute_from_color_names(beak_colors)),
    );
    attributes.insert(
        2,
        attribute_json("Eye", create_attribute_from_color_names(eye_colors)),
    );
    attributes.insert(
        3,
        attribute_json("Neck", create_attribute_from_color_names(neck_colors)),
    );
    attributes.insert(
        4,
        attribute_json("Back", create_attribute_from_color_names(back_colors)),
    );
    attributes.insert(
        5,
        attribute_json("Chest", create_attribute_from_color_names(chest_colors)),
    );
    attributes.insert(
        6,
        attribute_json("Wing", create_attribute_from_color_names(wing_colors)),
    );
    attributes.insert(
        7,
        attribute_json("Leg", create_attribute_from_color_names(leg_colors)),
    );

    // Now add the cocktributes
    for cocktribute in &cocktributes {
        let attribute_as_string = readable_cocktribute(cocktribute.clone());
        // Loop through the attribute vector
        for attribute in attribute_as_string {
            // Get the trait
            let _trait = attribute[0].clone();
            // Get the value
            let value = attribute[1].clone();
            if value == "None".to_string() {
                continue;
            }
            // Add the attribute to the attributes json
            attributes.insert(attributes.len(), attribute_json(_trait.as_str(), value));
            // attributes[_trait.as_str()] = attribute_json(_trait.as_str(), value);
        }
    }

    json!(attributes)
}
