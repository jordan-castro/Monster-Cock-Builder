#![allow(dead_code)]

use docopt::Docopt;
use serde::Deserialize;

mod gen;
mod hidden;
mod learning;
mod utils;

const USAGE: &'static str = "
MonsterCock Builder.

Usage: 
    mckbuilder gen <test> [--name=<name>] [--start=<start>] [--amount=<amount>] [--type=<type>] [--color=<color>]
    mckbuilder train <amount> [--type=<type>]

Options:
    -h, --help          Show this screen.
    --version           Show version.
    --name=<name>       The name of the MonsterCock.
    --start=<start>     The starting id for the MonsterCock.
    --amount=<amount>   The amount of cocks to generate.
    --type=<type>       The type of cock to draw.
    --color=<color>     The color category for the MonsterCock. 
";

#[derive(Debug, Deserialize)]
struct Args {
    flag_name: String,
    flag_start: u32,
    flag_amount: u32,
    flag_type: String,
    flag_color: String,
    cmd_gen: bool,
    cmd_train: bool,
    arg_test: Option<bool>,
    arg_amount: Option<u32>,
}

fn main() {
    let args: Args = Docopt::new(USAGE)
        .and_then(|d| d.deserialize())
        .unwrap_or_else(|e| e.exit());
    println!("{:?}", args);
}
