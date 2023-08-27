// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.8.18;

contract Notarization  {

   

    //Emitted when update function is called
    //Smart contract events are a way for your contract to communicate that something happened on the blockchain to your app front-end, which can be 'listening' for certain events and take action when they happen.
    event NewRate(uint serviceid, uint ratevalue, uint time);
    

    struct Rate {         
        uint service_id;
        uint user_id;
        uint rate_value;
        uint timestamp;
    }

    Rate rate;
    function setRate(uint service_id, uint user_id, uint rate_value, uint timestamp) public {
        rate = Rate(service_id,user_id,rate_value,timestamp);
        emit NewRate(service_id, rate_value, timestamp);
    }
    function getRateValue() public view returns (uint) {
        return rate.rate_value;
    }
    function getRateService() public view returns (uint) {
        return rate.service_id;
    }
    function getRateTime() public view returns (uint) {
        return rate.timestamp;
    }

    constructor() {
        
    }
}