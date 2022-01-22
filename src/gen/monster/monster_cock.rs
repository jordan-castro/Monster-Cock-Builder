use crate::gen::attributes::cocktributes::{CockTribute, attributes_json};
use crate::utils::image_utils::crop_image;
use crate::utils::randomify;

use crate::gen::canvas::base::Canvas;
use crate::gen::types::CockType;
use crate::gen::colors::CockColors;
use crate::utils::rgb_conversions::{rgba_to_rgb_u8, rgb_u8_to_i32, rgb_to_rgba_u8};
use crate::utils::names::black_list_name;

use image::{Rgba, RgbaImage, buffer::ConvertBuffer, imageops};
use rand::Rng;
use serde_json::{Map, Value, to_writer_pretty};

const DEFAULT_COCK: &str = "data/art/CockSepColors.png";
const SOLANA_COCK: &str = "data/art/Rooster2_HighRes.png";

/// The MonsterCock struct.
///
/// This is what handles the drawing of the monster cock.
///
#[derive(Debug, Clone)]
pub struct MonsterCock {
    canvas: Canvas,
    pub image: RgbaImage,
    pub name: String,
    pub id: u32,
    is_test_net: bool,
    pub hash: String,
    cock_colors: CockColors,
    cocktributes: Vec<CockTribute>
}

impl MonsterCock {
    pub (super) fn base(id: u32, generation: u32, cock_type: CockType, category: String, attributes: Option<Vec<CockTribute>>, is_test_net: bool) -> MonsterCock {
        let cocktributes = match attributes {
            Some(attributes) => 
                attributes,
            None => randomify::randomattributes(generation),
        };
        let cock_colors = CockColors::new(cock_type, category);
        // Create the canvas
        // Choose a random light_base value
        let light_base = rand::thread_rng().gen_range(0..2) == 1;
        let canvas = Canvas::new(light_base, false);

        MonsterCock {
            canvas,
            image: RgbaImage::new(0, 0),
            name: String::new(),
            id,
            is_test_net,
            hash: String::new(),
            cock_colors,
            cocktributes,
        }
    }

    /// Generates the MonsterCock.
    pub fn generate(&mut self) {
        self.canvas.draw_from_attributes(self.cocktributes.clone(), &mut self.cock_colors);
        // Create the image
        self.paste_cock_on_canvas();
        self.color_cock();
        // Mirror image?
        if self.cocktributes.contains(&CockTribute::SunRiseEast) {
            self.image = imageops::flip_horizontal(&self.image);
        }
    }

    /// Save the image to show later
    pub fn show_image(&mut self) -> bool {
        self.image.save("monstercock.png").expect("Saving image to monstercock.png");
        // Ask for user imput
        println!("Keep image? (y/n)");
        let mut input = String::new();
        std::io::stdin().read_line(&mut input).expect("Reading user input");
        if input.to_lowercase().trim() != "y" {
            std::fs::remove_file("monstercock.png").expect("Removing file");
            false
        } else {
            self.save();
            true
        }
    }

    /// Color the MonsterCock. Which means to change the colors of the image cock.
    fn color_cock(&mut self) {
        let convert_pixel = |pixel: Rgba<u8>| {
            rgb_u8_to_i32(rgba_to_rgb_u8(pixel.0))
        };
        let before_colors = self.cock_colors.before_colors();
        let after_colors = self.cock_colors.after_colors();
        // Loop through the pixels of the image
        for pixel in self.image.pixels_mut() {
            let color = convert_pixel(*pixel);
            // Check for color
            if before_colors.contains(&color) {
                let index = before_colors.iter().position(|&x| x == color).unwrap();
                // Change the color
                let color = after_colors.get(index).unwrap();
                let color = rgb_to_rgba_u8(*color);
                *pixel = Rgba([color[0], color[1], color[2], color[3]]);
            }
        }
    }

    /// Decides the name of the MonsterCock if it is not already set.
    fn name_cock(&mut self) {
        if self.name.is_empty() {
            let name = randomify::random_name(self.is_test_net);
            // Add the Id to the name
            self.name = format!("{} #{}", name, self.id);
        }
    }

    /// Place the cock on the canvas.
    fn paste_cock_on_canvas(&mut self) {
        // Crop the image
        self.canvas.image = crop_image(self.canvas.image.clone(), None);
        // Convert the canvas image to a Rgba
        let canvas_rgba = self.canvas.image.convert();

        let cock_image = match self.cock_colors.cock {
            CockType::Default => DEFAULT_COCK,
            CockType::Solana => SOLANA_COCK,
        };
        let cock_image = image::open(cock_image).expect("Opening cock image");
        self.image = paste_image_on_top(canvas_rgba, cock_image.into_rgba8());
    }

    /// Save the MonsterCock image.
    fn save(&mut self) {
        let cock_path = self.get_image_path();

        self.image.save(cock_path.as_str()).expect(format!("Saving MonsterCock image to {}", cock_path).as_str());
        self.save_cock_data();

        // Black list the name
        let name = self.get_idless_name();
        black_list_name(name, self.is_test_net);
    } 

    /// Save the cock data to a file LOCALLY.
    fn save_cock_data(&mut self) {
        let data = self.get_data();
        
        // Write to file
        let json_file = std::fs::File::create("attributes.json").unwrap();
        to_writer_pretty(json_file, &data).expect("C");
    }

    pub fn get_data(&mut self) -> Map<String, Value> {
        // Get attributes json format
        let attributes_json = attributes_json(self.cock_colors.colors.clone(), self.cocktributes.clone());        
        // A new map
        let mut data = Map::new();
        // Insert the JSON
        data.insert("image".to_string(), Value::String(self.get_image_path()));
        data.insert("name".to_string(), Value::String(self.name.clone()));
        data.insert("attributes".to_string(), attributes_json);
        data
    }

    /// Get the image path of the MonsterCock component.
    pub fn get_image_path(&mut self) -> String {
        self.name_cock();
        let mut file_parent = String::new();

        if self.is_test_net {
            file_parent.push_str("testnet");
        } else {
            file_parent.push_str("mainnet");
        }
        // The file name is as follows:
        // <name>_<id>.png
        let name = self.get_idless_name();

        format!("data/{}/{}_#{}.png", file_parent, name, self.id)
    }

    /// Get the cock name without the id.
    /// 
    /// # Returns
    /// `name: String` The name without the id.
    fn get_idless_name(&self) -> String {
        let name = self.name.clone();
        // Split off the id
        let name = name.split("#");
        let name = name.collect::<Vec<&str>>();
        // Trim the ending to remove any whitespace
        let name = name.get(0).unwrap().trim_end();
        name.to_string()
    }
    
}

/// Paste a image on top of another image.
///
/// # Params
/// - `image: &mut RgbImage` The image to paste on top of another image.
/// - `top_image: &mut RgbImage` The image to paste on top of another image.
///
/// # Returns
/// - `RgbImage` The image with the top image pasted on top of it.
fn paste_image_on_top(image: RgbaImage, top_image: RgbaImage) -> RgbaImage {
    println!("Pasting image");
    let mut new_image = image.clone();
    // Center of the image
    let center_x = image.width() / 2;
    let center_y = image.height() / 2;
    // Center of the top image
    let top_center_x = top_image.width() / 2;
    let top_center_y = top_image.height() / 2;

    // Overlay the image
    imageops::overlay(&mut new_image, &top_image, center_x - top_center_x, center_y - top_center_y);
    new_image
}