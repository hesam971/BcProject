        //  store the collected data
        const trackingData = {
            sections: [],
            scrollDepth: 0 // Initialize scroll depth to 0
        };
        
        //  store voting data for each section
        const votingData = {};
        const infoBoxInteractions = {};
        const keywordClickInteractions = {};

        // Get all section elements and the results div
        const sections = document.querySelectorAll('.section');
        const resultsDiv = document.getElementById('results');
        const infoButtons = document.querySelectorAll('.info-button');
        const infoBoxes = document.querySelectorAll('.info-box');
        const closeButtons = document.querySelectorAll('.close-button');

        let startTime = null;
        let currentSection = null;
        let timer = null;
        let timeoutId; // timeoutId in the global scope

        // Variable to track message 
        let helloWorldSent = false;

        // Function to track section changes and waiting time
        function trackSection(section) {
            if (currentSection !== section) {
                const currentTime = new Date();
                const sectionName = section.querySelector('h2').textContent;
                const waitTime = startTime ? ((currentTime - startTime) / 1000).toFixed(2) : 0;
                const localTime = currentTime.toLocaleTimeString();

                // Display a message when leaving the previous section
                if (currentSection) {
                    const previousSectionName = currentSection.querySelector('h2').textContent;
                    const leavingMessage = `Left ${previousSectionName}\nTime Spent in ${previousSectionName}: ${waitTime} seconds\nLocal Time: ${localTime}`;
                    console.log(leavingMessage);

                    // Append the leaving message to the tracking data object
                    trackingData.sections.push({
                        section: previousSectionName,
                        timeSpent: parseFloat(waitTime),
                        localTime
                    });
                }

                // Update the current section and start time
                currentSection = section;
                startTime = currentTime;

                // Clear the previous timer
                clearTimeout(timer);

                // Set a timer to check if the user needs help
                timer = setTimeout(() => {
                    // Close any open info boxes
                    infoBoxes.forEach(infoBox => {
                        infoBox.style.display = 'none';
                    });
                }, 50000);
            }
        }

        // intersection observer to track section changes
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    trackSection(entry.target);
                }
            });
        }, { threshold: 0.5 }); // Adjust the threshold as needed

        // Observing section elements
        sections.forEach(section => {
            observer.observe(section);
        });

        // event listener to show the information box when the button is clicked
        infoButtons.forEach((button, index) => {
            button.addEventListener('click', () => {
                infoBoxes[index].style.display = 'block';
                const sectionNumber = button.getAttribute('data-section');
                console.log(`Information box in Section ${sectionNumber} clicked`);
                
        // Record the time when the info-box was opened
        infoBoxInteractions[`section${sectionNumber}`] = {
            openedAt: new Date().toLocaleString(),
        };
            });
        });

        // event listener to close the information box when the close button is clicked
        closeButtons.forEach((button, index) => {
            button.addEventListener('click', () => {
                infoBoxes[index].style.display = 'none';
                const sectionNumber = button.getAttribute('data-section');
                console.log(`Information box in Section ${sectionNumber} closed`);
                
        // Record the time when the info-box was closed
        infoBoxInteractions[`section${sectionNumber}`].closedAt = new Date().toLocaleString();
            });
        });

        // Function to log keyword clicks
        function trackKeywordClick(keyword, sectionNumber) {
        console.log(`${keyword} clicked in information box in Section ${sectionNumber}`);

        // Store the interaction in the keywordClickInteractions object
        if (!keywordClickInteractions[`section${sectionNumber}`]) {
            keywordClickInteractions[`section${sectionNumber}`] = [];
        }

        keywordClickInteractions[`section${sectionNumber}`].push({
            keyword: keyword,
            timestamp: new Date().toLocaleString(),
        });
}

        // track keyword clicks in each info box
        infoBoxes.forEach((infoBox, index) => {
            const sectionNumber = index + 1; // Sections are 1-based
            const keywordLinks = infoBox.querySelectorAll('a');
            keywordLinks.forEach(link => {
                link.addEventListener('click', () => {
                    trackKeywordClick(link.textContent, sectionNumber);
                });
            });
        });

        // calculate and log scroll depth
        function logScrollDepth() {
            clearTimeout(timeoutId); // Clear any previous timeouts

            // Get the total scrollable height of the page
            const totalHeight = document.documentElement.scrollHeight - window.innerHeight;

            // Get the current scroll position
            const currentScroll = window.scrollY;

            // Calculate scroll depth as a percentage
            const scrollDepth = (currentScroll / totalHeight) * 100;

            // Log scroll depth to the console as soon as user stopped to scrolling / after a 5-second delay
            timeoutId = setTimeout(() => {
                console.log(`Scroll Depth: ${scrollDepth.toFixed(2)}%`);
                trackingData.scrollDepth = parseFloat(scrollDepth.toFixed(2)); // Update scroll depth in tracking data
            }, 5000); // 5000 milliseconds (5 seconds) delay
        }

        // event listener to measure scroll depth when the user scrolls
        window.addEventListener('scroll', logScrollDepth);

        var player;
      
        // YouTube Player API code asynchronously.
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
      
        // Called automatically when YouTube API code has loaded.
        function onYouTubeIframeAPIReady() {
          player = new YT.Player('my-video', {
            events: {
              'onStateChange': onPlayerStateChange
            }
          });
        }
      
        function onPlayerStateChange(event) {
          if (event.data == YT.PlayerState.PAUSED) {
            // Get the current time of the video
            var currentTime = player.getCurrentTime();
      
            // Get the total duration of the video
            var duration = player.getDuration();
      
            // Calculate the percentage of the video that the user has watched
            var percentageWatched = (currentTime / duration) * 100;
      
            // Log the percentage watched to the console
            console.log('The user has watched ' + percentageWatched.toFixed(2) + '% of the video');
            
            // Update the trackingData object with the video watching percentage
            trackingData.videoPercentage = parseFloat(percentageWatched.toFixed(2));
          }
        }
    


// Adding event listener for like and dislike buttons in each section
document.querySelectorAll('.section').forEach((section, index) => {
    const sectionNumber = index + 1;

    const likeButton = section.querySelector('.like-button');
    const dislikeButton = section.querySelector('.dislike-button');

    likeButton.addEventListener('click', () => {
        if (!votingData[sectionNumber]) {
            votingData[sectionNumber] = { likes: 1, dislikes: 0 };
            updateVoteCount(sectionNumber);
            console.log(`User liked section ${sectionNumber}`);
        }
    });

    dislikeButton.addEventListener('click', () => {
        if (!votingData[sectionNumber]) {
            votingData[sectionNumber] = { likes: 0, dislikes: 1 };
            updateVoteCount(sectionNumber);
            console.log(`User disliked section ${sectionNumber}`);
        }
    });
});

// update the vote count
function updateVoteCount(sectionNumber) {
    const likeButton = document.querySelector(`#section${sectionNumber} .like-button`);
    const dislikeButton = document.querySelector(`#section${sectionNumber} .dislike-button`);
    const voteData = votingData[sectionNumber];

    likeButton.textContent = `Like (${voteData.likes})`;
    dislikeButton.textContent = `Dislike (${voteData.dislikes})`;

    // Disable the buttons after voting
    likeButton.disabled = true;
    dislikeButton.disabled = true;
}

// Create an object to store the first interaction time for each section
const firstInteractionTime = {};

// Function to track the first interaction time for a section
function trackFirstInteraction(sectionNumber) {
    if (!firstInteractionTime[sectionNumber]) {
        const currentTime = new Date();
        const sectionName = `Section ${sectionNumber}`;
        const interactionTime = ((currentTime - startTime) / 1000).toFixed(2);
        console.log(`First interaction in ${sectionName} after ${interactionTime} seconds`);
        firstInteractionTime[sectionNumber] = interactionTime;
    }
}

// listeners to track first interaction for each section
document.querySelectorAll('.section').forEach((section, index) => {
    const sectionNumber = index + 1;
    section.addEventListener('click', () => {
        trackFirstInteraction(sectionNumber);
    });
});

// Create an object containing all the tracking data 
let exportData;

        // Function to send a message to the server
        function sendMessage() {
            if (!helloWorldSent) {
                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: 
                        
                    exportData = {
                        trackingData: trackingData,
                        votingData: votingData,
                        firstInteractionTime: firstInteractionTime,
                        infoBoxInteractions: infoBoxInteractions, 
                        videoPercentage: trackingData.videoPercentage,
                        keywordClickInteractions: keywordClickInteractions,
                    }},null, 2)
                    })
                .then(response => {
                    helloWorldSent = true;
                    return response.json();
                });
            }
        }

        // Initial message and interval to send data after 5 second
        setInterval(sendMessage, 5000);

        // update the data every 3 seconds
        setInterval(function () {
            fetch('/update_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: 
                        
                        exportData = {
                            trackingData: trackingData,
                            votingData: votingData,
                            firstInteractionTime: firstInteractionTime,
                            infoBoxInteractions: infoBoxInteractions, 
                            videoPercentage: trackingData.videoPercentage, 
                            keywordClickInteractions: keywordClickInteractions,
                        }},null, 2)
            })
            .then(response => response.json());
        }, 3000);