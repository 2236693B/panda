// var slideIndex = 1;
// showDivs(slideIndex);

// function plusDivs(n) {
    // showDivs(slideIndex += n);
// }

// function showDivs(n) {
    // var i;
    // var x = document.getElementsByClassName("mySlides");
    // if (n > x.length) {slideIndex = 1} 
    // if (n < 1) {slideIndex = x.length} ;
    // for (i = 0; i < x.length; i++) {
        // x[i].style.display = "none"; 
    // }
    // x[slideIndex-1].style.display = "block"; 
// }



















angular.module('app', ['cfp.hotkeys', 'nganimate'])
	.controller('maincontroller', function($scope, hotkeys) {
    
    	// functions
    	$scope.active = 0;
    
		$scope.previous = function() {
            if($scope.active != 0) $scope.active -= 1;
        }    
        
    	$scope.next = function() {
            if($scope.active + 1 < $scope.forests.length) $scope.active += 1;
        }
        
    	$scope.setactive = function(i) {
            $scope.active = i;
        }
    	
    	$scope.forests = [
            {
                'rank' : 1,
            	'name' : 'sagano bamboo forest',
                'desc' : 'a magnificent bamboo forest in the district of arashiyama, west to kyoto, japan.',
                'location' : 'kyoto, japan',
                'img' : 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/130891/sagano.jpg'
        	},
            {
                'rank' : 2,
            	'name' : 'giant sequoia national monument',
                'desc' : 'located in the southern sierra nevada mountains of california. the forest is named for the majestic giant sequoia  trees which populate 38 distinct groves within the boundaries of the forest. the sequoia national forest covers 4,829 sq km (1,865 sq mi).',
                'location' : 'california, united states',
                'img' : 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/130891/sequoia.jpg'
        	},
            {
                'rank' : 3,
            	'name' : 'redwood national park',
                'desc' : 'also in california, the redwood national parks is a combination of four parks that together protect 45% of all remaining coast redwood (sequoia sempervirens) old-growth forests, totaling at least 158 square km. these trees are the tallest and one of the most massive tree species on earth.',
                'location' : 'california, united states',
                'img' : 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/130891/redwoods.jpg'
        	},
            {
                'rank' : 4,
            	'name' : 'black forest',
                'desc' : 'schwarzwald or “black forest” is a wooded mountain range in baden-württemberg, southwestern germany. it is bordered by the rhine valley to the west and south. the name “black forest” was given by the romans who referred to the forest blocking out most of the sunlight from getting inside the forest by the dense growth of conifers.',
                'location' : 'germany',
                'img' : 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/130891/black-forest.jpg'
        	},
            {
                'rank' : 5,
            	'name' : 'crooked forest',
                'desc' : 'a grove of oddly-shaped pine trees. this young forest was planted around 1930 and has about 400 pines. it is generally believed that some form of human tool or technique was used to make the trees grow this way, but the method and motive are not currently known. some believe that the woods were deliberately grown this way to make “compass timbers”, or trees that are deliberately shaped for the purpose of using those odd shapes in ship building. another theory is that tanks from wwii are the cause, rolling over the young trees snapping the stem, but still surviving, forcing them to grow in the direction they were ran over.',
                'location' : 'poland',
                'img' : 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/130891/crooked-forest.jpg'
        	}
        ];
    
    	// hot keys
    	hotkeys.add({
            combo: 'right',
            description: 'next slide',
            callback: function() {
              $scope.next();
            }
        });
    	hotkeys.add({
            combo: 'left',
            description: 'previous slide',
            callback: function() {
              $scope.previous();
            }
        });
	});