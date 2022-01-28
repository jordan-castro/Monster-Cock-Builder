use image::{imageops, RgbaImage, RgbImage};
use rand::Rng;

use super::base::Canvas;


impl Canvas {
    /// Tile the current image.
    pub fn tile(&mut self) {
        let amount = rand::thread_rng().gen_range(1..50);

        let mut tile_image = RgbImage::new(self.image.width(), self.image.height());

        // Dimensions of image
        let width = self.image.width();
        let height = self.image.height();
        // Dimensions of tile
        let tile_width = width / amount;
        let tile_height = height / amount;

        // Make the tiles
        for xi in 0..amount {
            for i in 0..amount {
                // Choose a random x and Y coordinate
                let x1 = rand::thread_rng().gen_range(0..width);
                let y1 = rand::thread_rng().gen_range(0..height);

                // Get a random size, between 10 and 100
                let size = rand::thread_rng().gen_range(10..100);

                // Get a sub image
                let sub_image = imageops::crop(&mut self.image, x1, y1, size, size).to_image();
                // Now create a bottom for the tile
                let mut bottom_image = RgbImage::new(tile_width, tile_height);
                // Tile using sub image
                imageops::tile(&mut bottom_image, &sub_image);
                // Place the now bottom image onto the tile image
                imageops::overlay(
                    &mut tile_image,
                    &bottom_image,
                    tile_width * i,
                    tile_height * xi,
                );
            }
        }

        // Now set the image to the tile image
        self.image = tile_image;
    }

    /// Create a mosiac of the current image.
    pub fn create_mosiac(&mut self, image: &RgbaImage) {

    }
}
