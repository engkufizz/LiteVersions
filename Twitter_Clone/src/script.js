// Define an array to store the tweets
let tweets = [];

// Define a function to add a tweet to the array and display it
function addTweet(tweetText) {
	// Create a new tweet object
	let tweet = {
		id: Date.now(),
		text: tweetText,
		likes: 0
	};

	// Add the tweet to the beginning of the array
	tweets.unshift(tweet);

	// Display the tweets
	displayTweets();
}

// Define a function to display the tweets
function displayTweets() {
	// Get the tweets container element
	let tweetsContainer = document.querySelector('.tweets-container');

	// Clear the container
	tweetsContainer.innerHTML = '';

	// Loop through the tweets array and create a new element for each tweet
	for (let tweet of tweets) {
		// Create a new tweet element
		let tweetElement = document.createElement('div');
		tweetElement.classList.add('tweet');

		// Create a new text element and set its text content to the tweet text
		let textElement = document.createElement('p');
		textElement.textContent = tweet.text;

		// Append the text element to the tweet element
		tweetElement.appendChild(textElement);

		// Create a new like button element and set its text content to the number of likes
		let likeButton = document.createElement('button');
		likeButton.classList.add('like-button');
		likeButton.textContent = tweet.likes + ' likes';

		// Add a click event listener to the like button
		likeButton.addEventListener('click', function() {
			// Increment the number of likes
			tweet.likes++;

			// Update the like button text content
			likeButton.textContent = tweet.likes + ' likes';
		});

		// Append the like button to the tweet element
		tweetElement.appendChild(likeButton);

		// Append the tweet element to the tweets container
		tweetsContainer.appendChild(tweetElement);
	}
}

// Get the tweet button element
let tweetButton = document.querySelector('.tweet-button-container button');

// Add a click event listener to the tweet button
tweetButton.addEventListener('click', function() {
	// Get the tweet input element
	let tweetInput = document.querySelector('.tweet-input-container textarea');

	// Get the tweet text
	let tweetText = tweetInput.value;

	// Add the tweet to the array and display it
	addTweet(tweetText);

	// Clear the tweet input
	tweetInput.value = '';
});
