// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.18;



contract Feed4Cloud {

	
    struct Rating {
        uint serviceId;
        address userId;
        uint rating;
        uint timestamp;
    }

	Rating[] public allRatings;

    mapping (address => Rating[]) public userRatings;
	mapping (uint => Rating[]) public serviceRatings;	
	//added for final function
	mapping(address => Rating[]) public serviceIdRatings;


    function setRating(uint serviceId, uint rating) public {
        Rating memory newRating = Rating({
            serviceId: serviceId,
            userId: msg.sender,
            rating: rating,
            timestamp: block.timestamp
        });
        userRatings[msg.sender].push(newRating);
        serviceRatings[serviceId].push(newRating);
		//just added
		serviceIdRatings[msg.sender].push(newRating);
		allRatings.push(newRating);
    }

	//getRatings() returns all recorded ratings
	function getRatings() external view returns (Rating[] memory) {
		return allRatings;
	}


	//getUserRatings() returns the ratings assigned by a specific user with userId
	function getUserRatings(address userId) external view returns (Rating[] memory) {
	 require(userRatings[userId].length > 0, "No ratings found for this user.");
	 return userRatings[userId];
	}


	//getAverageUserRating() returns the average value of the ratings assigned by a specific user with userId
    function getAverageUserRating(address userId, uint serviceId) external view returns (uint) {
		require(userRatings[userId].length > 0, "No ratings found for this user.");
		uint total = 0;
		uint count = 0;
		for (uint i = 0; i < userRatings[userId].length; i++) {
			if (userRatings[userId][i].serviceId == serviceId) {
				total += userRatings[userId][i].rating;
				count++;
			}
		}
			return total/count;
     }

	 /*
	 //getAverageRatings() returns the average ratings of each user for a specific service
	 function getAverageRatings(uint serviceId) public view returns (uint[][] memory) {
		uint[userRatings.length][2] memory avgUserRatings;
		 for (uint i = 0; i < userRatings.length; i++) {
			avgUserRatings[i][0] = i;
			avgUserRatings[i][1] = getAverageUserRating(i,serviceId);
		}

		return avgUserRatings;
	 }
	 */

	//getServiceRatings() returns the ratings assigned to a specific service with serviceId
    function getServiceRatings(uint serviceId) public view returns (Rating[] memory) {
		require(serviceRatings[serviceId].length > 0, "No ratings found for this service.");
		return serviceRatings[serviceId];
    }

	//getLatestUserRating returns the latest rating by a specific user with userId that has been recorded
    function getLatestUserRating(address userId) public view returns (Rating memory) {
		Rating[] memory userRatingsByUserId = userRatings[userId];
		require( userRatingsByUserId.length > 0, "No ratings found for this user.");
        return userRatingsByUserId[userRatingsByUserId.length-1];
	}

	//added to return only the latest rating without the extra information about the users
	function getOnlyTheLatestUserRating(address userId) public view returns (uint) {
		Rating[] memory userRatingsByUserId = userRatings[userId];
		require( userRatingsByUserId.length > 0, "No ratings found for this user.");
        return userRatingsByUserId[userRatingsByUserId.length-1].rating;//vale .rating kai epistrefei uint
	}

	//getLatestServiceRating returns the latest rating for a specific service with serviceId that has been recorded
    function getLatestServiceRating(uint serviceId) public view returns (Rating memory) {
       Rating[] memory serviceRatingsByServiceId = serviceRatings[serviceId];
	   require(serviceRatingsByServiceId.length > 0, "No ratings found for this service.");
	   return serviceRatingsByServiceId[serviceRatingsByServiceId.length -1];
	}

	//added to return only the latest service rating without the extra information
    function getOnlyTheLatestServiceRating(uint serviceId) public view returns (uint) {
       Rating[] memory serviceRatingsByServiceId = serviceRatings[serviceId];
	   require(serviceRatingsByServiceId.length > 0, "No ratings found for this service.");
	   return serviceRatingsByServiceId[serviceRatingsByServiceId.length -1].rating;
	}

	//added to use in updateReputation function in Ratings_Composition
	function getLatestServiceId(address userId) public view returns(uint){
		Rating[] memory serviceIdByUserId=serviceIdRatings[userId];
		require(serviceIdByUserId.length > 0, "No ratings found for this service.");
		return serviceIdByUserId[serviceIdByUserId.length-1].serviceId;

	}
}

