use std::process::ExitCode;

use clap::Subcommand;
use color_eyre::Result;

use crate::config::Config;

pub(crate) mod init;
pub(crate) mod install;
pub(crate) mod run;

pub trait CliCommand {
	fn run(self, config: &Config) -> Result<ExitCode>;
}

#[derive(Subcommand)]
pub enum Command {
	Init(init::Command),
	Run(run::Command),
	Install(install::Command),
}

impl Command {
	pub fn run(self, config: &Config) -> Result<ExitCode> {
		match self {
			Self::Init(cmd) => cmd.run(config),
			Self::Run(cmd) => cmd.run(config),
			Self::Install(cmd) => cmd.run(config),
		}
	}
}

impl Default for Command {
	fn default() -> Self {
		Self::Run(run::Command::default())
	}
}
