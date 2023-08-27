//const API_KEY = process.env.API_KEY;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

// For Hardhat
const contract = require("../artifacts/contracts/Feed4Cloud.sol/Feed4Cloud.json");

// Provider
const provider = new ethers.providers.JsonRpcProvider("http://54.195.253.191:8545");

// Signer
const signer = new ethers.Wallet(PRIVATE_KEY, provider);

// Contract
const Feed4CloudSmartContract = new ethers.Contract(CONTRACT_ADDRESS, contract.abi, signer);

async function main() {
    
    var tx = await Feed4CloudSmartContract.setRating(1, 1, 3)
    await tx.wait();

    tx = await Feed4CloudSmartContract.setRating(1, 2, 4)
    await tx.wait();

    tx = await Feed4CloudSmartContract.setRating(2, 1, 3)
    await tx.wait();

    tx = await Feed4CloudSmartContract.setRating(2, 2, 5)
    await tx.wait();

    tx = await Feed4CloudSmartContract.setRating(2, 2, 2)
    await tx.wait();

    const ratings = await Feed4CloudSmartContract.getRatings();
    console.log(ratings);

    const userRatings = await Feed4CloudSmartContract.getUserRatings(2);
    console.log(userRatings);

    const avguserRatings = await Feed4CloudSmartContract.getAverageUserRating(2,2);
    console.log(avguserRatings); 

 //   const avgratings = await Feed4CloudSmartContract.getAverageRatings();
 //   console.log(avgratings);

    const serviceRatings = await Feed4CloudSmartContract.getServiceRatings(1);
    console.log(serviceRatings);

    const latestuserRating = await Feed4CloudSmartContract.getLatestUserRating(1);
    console.log(latestuserRating);

    const latestserviceRating = await Feed4CloudSmartContract.getLatestServiceRating(2);
    console.log(latestserviceRating);

    //const newValue = await Feed4CloudSmartContract.getRateValue();
    //console.log("The new rating value is: " + newValue);

    //const service = await Feed4CloudSmartContract.getRateService();
    //console.log("The rated service is: " + service);

    //const time = await Feed4CloudSmartContract.getRateTime();
    //console.log("The rate timestamp is: " + time);
  }
  main();