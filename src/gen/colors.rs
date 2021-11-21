use crate::gen::types::CockType;
use crate::hidden::globals::PALLETE_LOCATION;
use crate::utils::rgb_conversions::{rgb_name, hex_to_rgb};
use rand::Rng;
use serde_json::{Map, Value};


/// The color object of a Cocks Colors.
#[derive(Clone, Debug, PartialEq)]
pub struct Color {
    before: (i32, i32, i32),
    after: (i32, i32, i32),
    pub attribute_title: String,
    pub name: String,
}

impl Color {
    pub fn new(before: (i32, i32, i32), attribute_title: String) -> Color {
        Color {
            before,
            after: (1, 2, 3), // Defaulto
            attribute_title,
            name: String::from("No name"), // Defaulto
        }
    }
}

/// The cocks colors struct. Handles all color logic.
#[derive(Clone, Debug, PartialEq)]
pub struct CockColors {
    pub cock: CockType,
    pub colors: Vec<Color>,
    category: String,
    current_pallete: Vec<String>,
    palletes: Vec<Vec<String>>,
    pallete_colors_used: Vec<(i32, i32, i32)>,
    pub background: (i32, i32, i32),
}

impl CockColors {
    pub fn new(cock_type: CockType, category: String) -> CockColors {
        let mut cock_colors = CockColors {
            cock: cock_type,
            colors: Vec::new(),
            category: category,
            current_pallete: Vec::new(),
            palletes: Vec::new(),
            pallete_colors_used: Vec::new(),
            background: (0, 0, 0),
        };
        // Setup the palletes
        cock_colors.setup_palletes();
        // Setup the colors
        cock_colors.decide();
        // Return the cock colors
        cock_colors
    }

    /// Decide the colors that will be used for the cock.
    fn decide(&mut self) {
        let mut rgbs: Vec<(i32, i32, i32)> = vec![
            (148, 31, 61),
            (180, 63, 61),
            (213, 97, 53),
            (109, 12, 39),
            (247, 247, 239),
            (180, 77, 37),
            (239, 159, 88),
            (237, 129, 53),
            (24, 16, 56),
            (39, 37, 95),
            (56, 64, 116),
            (88, 89, 77),
            (120, 124, 120),
            (150, 129, 110),
            (126, 105, 102),
            (102, 81, 86),
        ];
        let mut attribute_titles: Vec<&str> = vec![
            "Comb", "Comb", "Beak", "Comb", "Eye", "Neck", "Back", "Back", "Chest", "Chest",
            "Wing", "Wing", "Wing", "Leg", "Leg", "Leg",
        ];

        // Check if we need to add the Spur
        if self.cock == CockType::Solana {
            rgbs.push((78, 65, 70));
            attribute_titles.push("Spur");
        }

        let mut colors: Vec<Color> = Vec::new();
        for rgb in rgbs.iter() {
            // El index del rgb para attribute_titles abajo
            let index = rgbs.iter().position(|x| x == rgb).unwrap();
            let color = Color::new(
                rgb.clone(),
                attribute_titles.get(index).unwrap().to_string(),
            );
            colors.push(color);
        }
        // Set the after and the name of the color for each color in colors
        for color in colors.iter_mut() {
            color.after = self.random_color_from_pallete();
            color.name = rgb_name(color.after);
        }
        // Set the colors
        self.colors = colors;
    }

    /// Grab the pallete_colors for a CockColors object.
    ///
    /// **Param**
    /// - `cock_colors: CockColors` The cock colors object.
    ///
    /// **Returns**
    /// - `Vec<Vec<(String, String, String, String)>>` The pallete colors.
    fn setup_palletes(&mut self) {
        // Grab palletes_json
        let palletes_json = get_palletes_json();

        // Get the pallete keys
        let category_keys: Vec<String> = palletes_json.keys().map(|x| x.to_string()).collect();
        // Check the category
        // The category is the key of the pallete. It can either be set by James manually or randomly chosen.
        if self.category.is_empty() {
            self.category = category_keys[rand::thread_rng().gen_range(0..category_keys.len())].to_string();
        }

        // println!("Category: {}", key);
        // Grab 4 random palletes from the category
        for _ in 0..4 {
            loop {
                // Grab a random pallete
                let pallete = pallete_from_category(&self.category);
                if self.add_new_pallete(pallete) {
                    break;
                }
            }
        }
        // Set the current palete to the first pallete
        self.current_pallete = self.palletes[0].clone();
    }

    /// Add a new pallete to the palletes.
    /// 
    /// **Params**
    /// - `pallete: Vec<String>` The pallete to add.
    /// 
    /// **Returns**
    /// - `bool` If the pallete was added.
    fn add_new_pallete(&mut self, pallete: Vec<String>) -> bool {
        // Check that the pallete is new
        if !self.palletes.contains(&pallete) {
            // Add the pallete to the palletes
            self.palletes.push(pallete);
            return true;
        }
        false
    }

    /// Grab a random color from the pallete.
    ///
    /// **Param**
    /// - `cock_colors: CockColors` The cock colors object.
    ///
    /// **Returns**
    /// - `rgb_color: (red, green, blue)`.
    pub fn random_color_from_pallete(&mut self) -> (i32, i32, i32) {
        loop {
            // Grab a random color from the current pallete
            let pallete_color = color_from_pallete(&self.current_pallete);
            // Check its a new pallete_color
            if !self.pallete_colors_used.contains(&pallete_color) {
                // Add the pallete_color to the pallete_colors_used
                self.pallete_colors_used.push(pallete_color);
                // Return the pallete_color
                return pallete_color;
            } else {
                // Check the index of the pallete
                let index = self.palletes.iter().position(|x| x == &self.current_pallete).unwrap();
                // Check if less than length of palletes
                if index < self.palletes.len() - 1 {
                    // Set the current pallete to the next pallete
                    self.current_pallete = self.palletes[index + 1].clone();
                } else {
                    // Add a new pallete
                    loop {
                        // Grab a random pallete
                        let pallete = pallete_from_category(&self.category);
                        if self.add_new_pallete(pallete) {
                            break;
                        }
                    }
                }
            }
        }
    }

    ///
    /// Get the before colors of the cock
    /// 
    /// # Returns
    /// - `Vec<(i32, i32, i32)>` The before colors of the cock.
    /// 
    pub fn before_colors(&self) -> Vec<(i32, i32, i32)> {
        let mut before_colors: Vec<(i32, i32, i32)> = Vec::new();
        for color in self.colors.iter() {
            before_colors.push(color.before);
        }
        before_colors
    }

    /// 
    /// Get the after colors of the cock
    /// 
    /// # Returns
    /// - `Vec<(i32, i32, i32)>` The after colors of the cock.
    /// 
    pub fn after_colors(&self) -> Vec<(i32, i32, i32)> {
        let mut after_colors: Vec<(i32, i32, i32)> = Vec::new();
        for color in self.colors.iter() {
            after_colors.push(color.after);
        }
        after_colors
    }
}

/// The JSON file with the palletes.
///
/// **Returns:** `&Map<String, Value>`.
fn get_palletes_json() -> Map<String, Value> {
    // Open the Pallete file and convert to a JSON object
    let pallete_file = std::fs::read_to_string(PALLETE_LOCATION).unwrap();
    let pallete_json: serde_json::Value = serde_json::from_str(&pallete_file).unwrap();
    let pallete_json = pallete_json.as_object().unwrap();

    // Return the json as a clone
    pallete_json.clone()
}

/// Grab a random pallete from a category.
///
/// **Params**
/// - `category: &String` The category of the pallete.
///
/// **Returns**
/// - `pallete: Vec<String>` The pallete.
fn pallete_from_category(category: &String) -> Vec<String> {
    // Grab JSON
    let palletes_json = get_palletes_json();
    // Grab the palletes of the category
    let category_palletes = palletes_json.get(category).unwrap().as_object().unwrap();

    // Grab the length of the palletes that are in the category
    let length_of_palletes_in_category = category_palletes.len();

    let pallete_index = rand::thread_rng()
        .gen_range(0..length_of_palletes_in_category)
        .to_string();
    // Grab the pallete chosen based on the index
    let pallete = category_palletes
        .get(&pallete_index)
        .unwrap()
        .as_array()
        .unwrap();
    // Convert (Cast) pallete to a Vec<String>
    let pallete = pallete
        .iter()
        .map(|x| x.as_str().unwrap().to_string())
        .collect();
    pallete
}

/// Grab a single random color from a pallete
///
/// **Params**
/// - `pallete: Vec<String>` The pallete.
///
/// **Returns**
/// - `rgb_color: (red, green, blue)`.
fn color_from_pallete(pallete: &Vec<String>) -> (i32, i32, i32) {
    // Grab a random index out of the length of the pallete
    let index = rand::thread_rng().gen_range(0..pallete.len());
    let hex_color = pallete.get(index).unwrap();
    // Convert the hex color to a rgb color
    let rgb_color = hex_to_rgb(hex_color.as_str());
    rgb_color
}
