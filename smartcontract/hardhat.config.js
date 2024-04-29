require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
	solidity: {
		compilers: [
			{ version: "0.5.7" },
			{ version: "0.6.7", settings: {} },
			{ version: "0.8.0", settings: {} }, // Add this line.
			{ version: "0.8.19", settings: {} }, // Add this line.
			{ version: "0.8.20", settings: {} }, // Add this line.
		],
	},
	networks: {
		ganache: {
			url: process.env.PROVIDER_URL,
			accounts: [process.env.PRIVATE_KEY],
			gas:"auto"
		},
	},
};
