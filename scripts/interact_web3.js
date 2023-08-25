// JavaScript source code
const Web3 = require('web3');
const web3 = new Web3('http://127.0.0.1:7545'); 

const abi = require('C:/Users/super/Desktop/feed4cloudProjects/feed4cloud_weight_6/feed4Cloud.json'); 
const Feed4CloudSmartContractAddress = '0x2D12ddc3A8cF91042340194eff01ff831119EDe4'; 

const Feed4CloudSmartContract = new web3.eth.Contract(abi, Feed4CloudSmartContractAddress);

const schedule = require('node-schedule');

let on = true;
let attackerRating;
let secondattackerRating;
let thirdattackerRating;

function on_off() {

    let onTime;
    

    on = !on;   

    if (on) {
        console.log('Attack is on!');
        onTime = Math.floor(Math.random() * 3 * (10 ** 5)) + (3 * (10 **5));
    }
    else {
        console.log('Attack is off!');
        onTime = Math.floor(Math.random() * 3 * (10 ** 5)) + (3 * (10 ** 5));    
    }    
    console.log(`next behavior change in ${onTime/60000} minutes`);
    setTimeout(on_off, onTime);
}



async function submitRatings() {
    const accounts =await web3.eth.getAccounts();

    const user1 = accounts[0];
    const user2 = accounts[1];
    const user3 = accounts[2];
    const user4 = accounts[3];
    const user5 = accounts[4];
    const user6 = accounts[5];
    const user7 = accounts[6];
    const user8 = accounts[7];
    const user9 = accounts[8];

    console.log("Submitting ratings..");

    if(on){
            attackerRating=2;
            secondattackerRating=2;
            thirdattackerRating=2;
    }
    else{
        attackerRating=5;
        secondattackerRating=5;
        thirdattackerRating=5;
    }
    

    console.log('attacker is:');
    console.log(user1);
    console.log(user2);
    console.log(user3);
    var tx = await Feed4CloudSmartContract.methods.setRating(74178, attackerRating).send({ from: user1, gas: 1000000 });

    tx = await Feed4CloudSmartContract.methods.setRating(74178, secondattackerRating).send({ from: user2, gas: 1000000 });
    
    tx = await Feed4CloudSmartContract.methods.setRating(74178, thirdattackerRating).send({ from: user3, gas: 1000000 });
    
    tx = await Feed4CloudSmartContract.methods.setRating(74178, 5).send({ from: user4, gas: 1000000 });
 
    tx = await Feed4CloudSmartContract.methods.setRating(74178, 5).send({ from: user5, gas: 1000000 });
   
    tx = await Feed4CloudSmartContract.methods.setRating(74178, 5).send({ from: user6, gas: 1000000 });

    tx = await Feed4CloudSmartContract.methods.setRating(74178, 5).send({ from: user7, gas: 1000000 });

    tx = await Feed4CloudSmartContract.methods.setRating(74178, 5).send({ from: user8, gas: 1000000 });

    tx = await Feed4CloudSmartContract.methods.setRating(74178, 5).send({ from: user9, gas: 1000000 });
    
    const ratings = await Feed4CloudSmartContract.methods.getRatings().call();
    console.log(ratings);

    //const userRatings = await Feed4CloudSmartContract.methods.getUserRatings(user2).call();
    //console.log(userRatings);

    //const avguserRatings = await Feed4CloudSmartContract.methods.getAverageUserRating(user2, 2).call();
    //console.log(avguserRatings); 

    //const serviceRatings = await Feed4CloudSmartContract.methods.getServiceRatings(1).call();
    //console.log(serviceRatings);

    //const latestuserRating = await Feed4CloudSmartContract.methods.getLatestUserRating(user1).call();
    //console.log(latestuserRating);

    //const latestserviceRating = await Feed4CloudSmartContract.methods.getLatestServiceRating(2).call();
    //console.log(latestserviceRating);

}
async function main(){

    on_off();
    // call every 1 minutes
    schedule.scheduleJob('*/1 * * * *', () => {
        submitRatings();
    });   
}

main();