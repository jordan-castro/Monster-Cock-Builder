use crate::gen::attributes::cocktributes::{CockTribute, attributes_json};
use crate::utils::randomify;

use crate::gen::canvas::base::Canvas;
use crate::gen::types::CockType;
use crate::gen::colors::CockColors;
use crate::utils::rgb_conversions::{rgba_to_rgb_u8, rgb_u8_to_i32, rgb_to_rgba_u8};
use crate::utils::names::black_list_name;

use image::{Rgba, RgbaImage, buffer::ConvertBuffer, imageops};
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
    image: RgbaImage,
    pub name: String,
    pub id: u32,
    is_test_net: bool,
}

impl MonsterCock {
    pub (super) fn base(id: u32, generation: i32, cock_type: CockType, category: String, attributes: Option<Vec<CockTribute>>, is_test_net: bool) -> MonsterCock {
        let cock_tributes = match attributes {
            Some(attributes) => attributes,
            None => randomify::randomattributes(generation),
        };
        let cock_colors = CockColors::new(cock_type, category);
        // Create the canvas
        let canvas = Canvas::new(cock_tributes, cock_colors, true, false);

        MonsterCock {
            canvas: canvas,
            image: RgbaImage::new(0, 0),
            name: String::new(),
            id: id,
            is_test_net: is_test_net,
        }
    }

    /// Generates the MonsterCock.
    pub fn generate(&mut self) {
        self.canvas.draw_canvas();
        // Create the image
        self.paste_cock_on_canvas();
        self.color_cock();
        // Mirror image?
        match self.canvas.cocktributes.last().unwrap() {
            CockTribute::Sun { rising } => {
                if rising == &true {
                    // Mirror the image
                    self.image = imageops::flip_horizontal(&self.image);
                }
            },
            _ => {},
        }
    }

    /// Decides the name of the MonsterCock if it is not already set.
    fn name_cock(&mut self) {
        if self.name.is_empty() {
            self.name = randomify::random_name(self.is_test_net);
            // Add the Id to the name
            self.name = format!("{} #{}", self.name, self.id);
        }
    }

    /// Place the cock on the canvas.
    fn paste_cock_on_canvas(&mut self) {
        // Convert the canvas image to a Rgba
        let canvas_rgba = self.canvas.image.convert();

        if self.canvas.cock_colors.cock == CockType::Default {
            // Default cock
            let cock_image = image::open(DEFAULT_COCK).unwrap();
            // Paste the cock_image on a Red image
            self.image =
                paste_image_on_top(canvas_rgba, cock_image.into_rgba8());
        } else if self.canvas.cock_colors.cock == CockType::Solana {
            // Solana cock
            let cock_image = image::open(SOLANA_COCK).unwrap();
            // Paste the cock_image on a Red image
            self.image =
                paste_image_on_top(canvas_rgba, cock_image.into_rgba8());
        } else {
            panic!(
                "CockType : {:?} not implemented!",
                self.canvas.cock_colors.cock
            );
        }
    }

    ///
    /// Color the MonsterCock. Which means to change the colors of the image cock.
    /// 
    fn color_cock(&mut self) {
        let convert_pixel = |pixel: Rgba<u8>| {
            rgb_u8_to_i32(rgba_to_rgb_u8(pixel.0))
        };
        let before_colors = self.canvas.cock_colors.before_colors();
        let after_colors = self.canvas.cock_colors.after_colors();
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

    /// Save the image to show later
    pub fn show_image(&mut self) {
        self.image.save("monstercock.png").expect("Saving image to monstercock.png");
        // Ask for user imput
        println!("Keep image? (y/n)");
        let mut input = String::new();
        std::io::stdin().read_line(&mut input).expect("Reading user input");
        if input.to_lowercase().trim() != "y" {
            std::fs::remove_file("monstercock.png").expect("Removing file");
        } else {
            self.save();
        }
    }

    /// Save the MonsterCock image.
    pub fn save(&mut self) {
        let cock_path = self.get_image_path();

        self.image.save(cock_path.as_str()).expect(format!("Saving MonsterCock image to {}", cock_path).as_str());
        // Black list the name
        let name_to_black_list = self.name.split("#").collect::<Vec<&str>>();
        let name = name_to_black_list.get(0).unwrap();
        black_list_name(name.to_string(), self.is_test_net);
        self.save_cock_data();
    } 

    /// Get the image path of the MonsterCock component.
    fn get_image_path(&mut self) -> String {
        self.name_cock();
        let mut file_parent = String::new();

        if self.is_test_net {
            file_parent.push_str("testnet");
        } else {
            file_parent.push_str("mainnet");
        }

        format!("data/{}/{}.png", file_parent, self.name)
    }

    /// Save the cock data to a file.
    fn save_cock_data(&mut self) {
        let attributes_json = attributes_json(self.canvas.cock_colors.colors.clone(), self.canvas.cocktributes.clone());        
        let mut data = Map::new();
        data.insert("image".to_string(), Value::String(self.get_image_path()));
        data.insert("name".to_string(), Value::String(self.name.clone()));
        data.insert("attributes".to_string(), attributes_json);
        
        // Write to file
        let json_file = std::fs::File::create("attributes.json").unwrap();
        to_writer_pretty(json_file, &data).expect("C");
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