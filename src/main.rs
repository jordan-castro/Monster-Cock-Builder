#![allow(dead_code)]

use docopt::Docopt;
use gen::monster::monster_cock::MonsterCock;
use learning::data_set::training_data;
use serde::Deserialize;

use crate::{gen::types::CockType, hidden::upload::upload_to_ipfs};

mod gen;
mod hidden;
mod learning;
mod utils;

const USAGE: &'static str = "
MonsterCock Builder.

Usage: 
    mckbuilder gen <chain> [--name=<name>] [--start=<start>] [--amount=<amount>] [--type=<type>] [--color=<color>] [--upload]
    mckbuilder train <amount>
    mckbuilder (-h | --help)
    mckbuilder --version

Options:
    -h, --help          Show this screen.
    --version           Show version.
    --name=<name>       The name of the MonsterCock.
    --start=<start>     The starting id for the MonsterCock.
    --amount=<amount>   The amount of cocks to generate.
    --type=<type>       The type of cock to draw.
    --color=<color>     The color category for the MonsterCock. 
    --upload            Upload the generated MonsterCock to the IPFS node.
";

#[derive(Debug, Deserialize)]
struct Args {
    flag_name: String,
    flag_start: u32,
    flag_amount: u32,
    flag_type: String,
    flag_color: String,
    flag_upload: bool,
    cmd_gen: bool,
    cmd_train: bool,
    arg_chain: Option<u32>,
    arg_amount: Option<u32>,
}

#[tokio::main]
async fn main() {
    let args: Args = Docopt::new(USAGE)
        .and_then(|d| d.deserialize())
        .unwrap_or_else(|e| e.exit());

    if args.cmd_gen {
        let chain = args.arg_chain.unwrap();
        let name = args.flag_name;
        let start = args.flag_start;
        let amount = args.flag_amount;
        let type_ = args.flag_type;
        let color = args.flag_color;
        let upload = args.flag_upload;

        // Check amount is set
        if amount != 0 {
            panic!("Amount not implemented yet!");
        }
        if start == 0 {
            panic!("If creating the first monster cock for this chain, Please run the command with the --new flag.")
        }

        // Check the test_net based on the chain id passed
        let is_test_net = match chain {
            80001 => true,
            137 => false,
            _ => panic!(
                "Invalid chain id: {}, This chain has not been implemented yet!",
                chain
            ),
        };
        let cock_type = match type_.to_lowercase().as_str() {
            "default" => CockType::Default,
            "def" => CockType::Default,
            "solana" => CockType::Solana,
            "sol" => CockType::Solana,
            _ => CockType::Default, // Default cock es the default
        };
        generate_monster_cock(name, start, cock_type, color, is_test_net, upload).await;
    } else if args.cmd_train {
        let amount = args.arg_amount.unwrap();
        training_data(amount);
    }
}

/// Generate a monstercock.
///
/// # Params
/// - `name: String` The name of the cock.
/// - `id: u32` The id of the cock
/// - `cock_type: CockType` The type of cock.
/// - `color_category: String` The color category of the cock.
/// - `is_test_net: bool` Is the cock on the test net?
/// - `upload: bool` Should we upload this MCK to the IPFS?
async fn generate_monster_cock(
    name: String,
    id: u32,
    cock_type: CockType,
    color_category: String,
    is_test_net: bool,
    upload: bool,
) {
    let mut cock: MonsterCock;
    if !name.is_empty() && !color_category.is_empty() {
        cock = MonsterCock::with_name_and_category(
            id,
            cock_type,
            name,
            color_category,
            is_test_net,
        );
    } else if !name.is_empty() {
        cock = MonsterCock::with_name(id, cock_type, name, is_test_net);
    } else if !color_category.is_empty() {
        cock = MonsterCock::with_category(id, cock_type, color_category, is_test_net);
    } else {
        cock = MonsterCock::new(id, cock_type, is_test_net);
    }

    // Generate and save cock
    cock.generate();
    // Show handles the saving and user input shit
    let saved = cock.show_image();
    if saved && upload {
        // Poll future
        upload_cock(&mut cock).await;
    }
}

async fn upload_cock(cock: &mut MonsterCock) {
    // If the upload flag is set, upload the generated MonsterCock to the IPFS node.
    let hashes = upload_to_ipfs(cock).await;
    match hashes {
        Ok(hashes) => {
            println!("Upload to IPFS successfull");
            println!("Hashes are: ");
            println!("Json Hash: {}, \nImage Hash: {}", hashes.1, hashes.0);
        }
        Err(e) => {
            println!("Error uploading to IPFS: {:?}", e);
        }
    }
}
