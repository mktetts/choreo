const hre = require("hardhat");
const fs = require("fs");

async function main() {
	const DoctorDetailContract = await hre.ethers.getContractFactory("DoctorDetailContract");
	let doctorDetailContract = await DoctorDetailContract.deploy();
	console.log("DoctorDetail contract address:", doctorDetailContract.target);

	
	const PrescriptionDetailContract = await hre.ethers.getContractFactory("PrescriptionDetailContract");
	let prescriptionDetailContract = await PrescriptionDetailContract.deploy();
	console.log("PrescriptionDetail contract address:", prescriptionDetailContract.target);
	
	moveContractFiles(prescriptionDetailContract, "PrescriptionDetailContract");
	moveContractFiles(doctorDetailContract, "DoctorDetailContract");
}

function moveContractFiles(contract, name) {
	const contractsDir = __dirname + "/../../flask/app/blockchain/contractsData";

	if (!fs.existsSync(contractsDir)) {
		fs.mkdirSync(contractsDir);
	}

	fs.writeFileSync(
		contractsDir + `/${name}_address.json`,
		JSON.stringify({ address: contract.target }, undefined, 2)
	);

	const contractArtifact = artifacts.readArtifactSync(name);

	fs.writeFileSync(
		contractsDir + `/${name}.json`,
		JSON.stringify(contractArtifact, null, 2)
	);
}

main().catch((error) => {
	console.error(error);
	process.exitCode = 1;
});
