// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.18;
import "./Feed4Cloud.sol";



contract RatingsAndComposition{
    //variables
    uint fakes;
    uint total;
    uint ReputationScore; 

    mapping(address => bool) public credibilitySupervisor; //add the supervisor here
    mapping(address =>uint) public userFakes;         //getfakes used to compute credibility
    mapping(address =>uint) public userCredibility;    //credibility of specific user
    mapping(address =>uint) public userTotal;         //getotal used to compute credibility
    mapping(address => uint) public credibilRating;

    modifier onlyCredibilitySupervisor(address _supervisor){
        require(credibilitySupervisor[_supervisor]);
        _;
    }

    //set a supervisor for the credibility and reputation mechanisms
    function setCredibilitySupervisor(address supervisor) public returns(address h){
        credibilitySupervisor[supervisor]=true;
        return supervisor;
    }

    //increment Fakes everytimes punish!=0
    function setFakes(address supervised) public onlyCredibilitySupervisor(msg.sender) returns(uint x1){
        fakes=getFakes(supervised)+1;
        userFakes[supervised]=fakes;
        return userFakes[supervised];
    }
    function getFakes(address supervised) public view returns (uint x1){
        return userFakes[supervised];
    }

    //increment total in every credibility update
    function setTotal(address supervised) public onlyCredibilitySupervisor(msg.sender) returns(uint x1){
        total=getTotal(supervised)+1;
        userTotal[supervised]=total;
        return userTotal[supervised];
    }
    function getTotal(address supervised) public view returns (uint x1){
        return userTotal[supervised];
    }

    //calculate Credibility Rating
    function Credibility_rating(int punish,address supervised) public returns(uint b1){
        if(punish==0){       
            credibilRating[supervised]=100;
        }
        else{                
            uint theFakes =userFakes[supervised]*100; 
            uint theTotal=userTotal[supervised]; 
            credibilRating[supervised]=100-theFakes/theTotal;  
        }
        if(credibilRating[supervised]>100){
            credibilRating[supervised]=100;
        }
        else if(credibilRating[supervised]<0 || credibilRating[supervised]==0){
            credibilRating[supervised]=1;
        }
        return credibilRating[supervised];
    }

    function getCredibilityRating(address supervised) public view returns (uint b1) {
        return credibilRating[supervised];
    }


    //calculate user Credibility
    function update_Credibility(address supervised) public onlyCredibilitySupervisor(msg.sender) returns(uint y){
        uint w=6;
        if(userCredibility[supervised]==0){
            userCredibility[supervised]=50;//egine diorwthwsi
        }
        uint credibility=w*userCredibility[supervised]+(10-w)* credibilRating[supervised];
        userCredibility[supervised]=credibility/10;
        if(userCredibility[supervised]<1){
            userCredibility[supervised]=1;
        }
        else if(userCredibility[supervised]>100){
            userCredibility[supervised]=100;
        }
        return (userCredibility[supervised]);
    }

    function getCredibility(address supervised) public view returns (uint x) {
        return userCredibility[supervised] ;
    }

    //calculate service Reputation Score
    function update_Reputation(address supervised,uint rating) public onlyCredibilitySupervisor(msg.sender) returns(uint t){
        ReputationScore=(100-userCredibility[supervised])*ReputationScore+userCredibility[supervised]*rating;
        ReputationScore=ReputationScore/100;
       if(ReputationScore<1){
            ReputationScore=1;
        }
        else if(ReputationScore>100){
            ReputationScore=100;
        }
        return ReputationScore;
    } 

    function getReputationScore() public view returns (uint x) {
        return ReputationScore ;
    }


}