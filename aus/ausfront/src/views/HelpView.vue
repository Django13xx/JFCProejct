<template>
  <div>
    <!-- Teaching Mode Features Help Page -->
    <div class="help-page">
      <div class="header">
        <h1><i class="fas fa-chalkboard-teacher"></i> Explore the Teaching Mode</h1>
      </div>
      <div class="content">
        <section>
          <h2><i class="fas fa-info-circle"></i> Introduction</h2>
          <strong>
            Welcome to our Teaching Mode! This powerful tool allows you to manage audio tracks active in the auscultation model efficiently, enhancing your experience in auscultation learning and practicing.
          </strong>
        </section>

        <section>
          <h2 class="colorOrange quick-start-guide"><i class="fas fa-rocket"></i> Quick Start Guide</h2>
          <ul>
            <li><strong class="colorOrange"><i class="fas fa-chevron-left"></i><i class="fas fa-chevron-right"></i> Switch Current List:</strong> Use the left and right chevron buttons to navigate between different views in the audio table.</li>
            <li><strong class="colorOrange"><i class="fas fa-arrow-left"></i> Add Audio to Current List:</strong> Click on the orange arrow button to add the selected audio to your "Current List."</li>
            <li><strong class="colorOrange"><i class="fas fa-play"></i> Activate/Deactivate Audio:</strong> Toggle the play icon to activate or deactivate a specific audio track in your "Current List."</li>
          </ul>
        </section>

        <section>
          <h2><i class="fas fa-music"></i> Audio Library</h2>
          <ul>
            <li><strong class="colorOrange"><i class="fas fa-arrow-left"></i> Add to List:</strong> Incorporate audio tracks into your selected list. Successful additions are indicated by the grey arrow turning orange.</li>
            <li><strong> Selected Audios are added to your “Current List”</strong></li>
            <li><strong> Library Table:</strong> Browse detailed information about available audio tracks to make informed selections.</li>
            <li><strong> Searching and Sorting:</strong> Searching by the searching bar with different searching options, sorting by clicking on table header attributes</li>
            <li><strong class="colorOrange"> <i class="fas fa-pencil-alt"></i> Edit Button:</strong> Refine your audio files by adjusting their title, description, grading, and categorization. Additionally, remove/delete them from the audio library.</li>
          </ul>
        </section>

        <section>
          <h2><i class="fas fa-table"></i> Current List Content</h2>
          <ul>
            <li><strong class="colorOrange"><i class="fas fa-play"></i> Active:</strong> Toggle to apply or unapply the selected audio track for a more personalized experience.</li>
            <li><strong><i class="fas fa-trash-alt"></i> Remove:</strong> Safely remove the selected audio track from the current list to streamline your content.</li>
          </ul>
        </section>

        <section>
          <h2><i class="fas fa-list"></i> Current List Management</h2>
          <ul>
            <li><strong><i class="fas fa-plus"></i> Create New List:</strong> Easily create a new list to organize specific audio tracks.</li>
            <li><strong><i class="fas fa-pencil-alt"></i> Rename List:</strong> Customize list names for easy identification and personalization.</li>
            <li><strong><i class="fas fa-trash-alt"></i> Remove List:</strong> Safely delete unwanted lists (except the last one).</li>
          </ul>
        </section>
      </div>
    </div>

    <!-- Auscultation Practice System Help Page -->
    <div class="help-page">
      <div class="header">
        <h1><i class="fas fa-stethoscope"></i> Auscultation Practice System</h1>
      </div>

      <div class="content">
        <section>
          <h2><i class="fas fa-info-circle"></i> Introduction</h2>
          <p>
            Welcome to our Auscultation System! This innovative platform is designed to make learning and practicing the auscultation process for a dog's heartbeat and lung sounds a seamless experience. Below, you'll find a guide to help you get started and make the most out of our simulation.
          </p>
        </section>

        <section>
          <h2><i class="fas fa-play-circle"></i> Getting Started</h2>
          <ul>
            <li><strong><i class="fas fa-heartbeat"></i> Status Icons:</strong> The heart and lung icons are your gateways to specific auscultation areas. Click on these icons to activate or deactivate listening modes for a more focused simulation.</li>
            <li><strong><i class="fas fa-sliders-h"></i> Control Panel:</strong> Navigate through different listening modes with ease using the buttons in the control panel. Whether you're focusing on Heartbeat Count, Abnormal Identification, or prefer the Mixed Mode.</li>
            <li><strong><i class="fas fa-mouse-pointer"></i> Interaction Area:</strong> Engage with the simulation on a deeper level in this dedicated space. Explore questions, find answers, and interact with elements that enhance your understanding of the auscultation process.</li>
          </ul>
        </section>

        <section>
          <h2><i class="fas fa-sliders-h"></i> Control Panel</h2>
          <p>
            The control panel houses the following buttons:
          </p>
          <ul>
            <li><strong><i class="fas fa-heart"></i> Heart:</strong> Play the heartbeat sound <strong>(set as default)</strong>, the one active in Teaching Dashboard</li>
            <li><strong><i class="fas fa-lungs"></i> Lungs:</strong> Play the lung sound <strong>(set as default)</strong>, the one active in Teaching Dashboard</li>
          </ul>
          <p>Click on the buttons to seamlessly switch between desired listening modes.</p>
        </section>

        <section>
          <h2><i class="fas fa-headphones-alt"></i> Listening Modes</h2>
          <p>
            Our system offers three main listening modes:
          </p>
          <ul>
            <li><strong><i class="fas fa-heartbeat"></i> Heartbeat Mode:</strong> Swap current Heartbeat audio for different sounds to practice heartrate counting.</li>
            <li><strong><i class="fas fa-biohazard"></i> Abnormal Identification:</strong> Train your skills to identify abnormal sounds in both the heart and lung regions.</li>
            <li><strong><i class="fas fa-sync"></i> Mixed Mode:</strong> Experience a comprehensive simulation by listening to both the heart and lung areas simultaneously. Providing a challenging simulation for practical auscultation training.</li>
          </ul>
          <p>Toggle between these modes effortlessly using the buttons in the control panel.</p>
        </section>

        <section>
          <h2><i class="fas fa-mouse-pointer"></i> Interaction Area</h2>
          <p>
            <ul>
              <li><strong><i class="fas fa-puzzle-piece"></i> Interactive Elements:</strong> Engage with quizzes or scenarios that test and enhance your skills.</li>
              <li><strong><i class="fas fa-info-circle"></i> Additional Information:</strong> Discover supplementary details to deepen your understanding.</li>
            </ul>
          </p>
        </section>

        <section>
          <h2><i class="fas fa-question-circle"></i> Frequently Asked Questions (FAQ)</h2>
          <ul>
            <li><strong>Q:</strong> How do I activate a listening mode?</li>
            <li><strong>A:</strong> Click on the respective heart or lung icon to activate the desired listening mode. Use the control panel buttons for specific listening modes.</li>
            <!-- Add more FAQs as needed -->
          </ul>
        </section>
      </div>
    </div>
  </div>
</template>

  
  <style scoped>
  .help-page {
    display: flex;
    flex-direction: column;
    background-color: #f0f0f0; /* Grey background */
    color: #333; /* Dark text color */
    padding: 20px;
    font-family: 'Arial', sans-serif;
    margin-bottom: 20px;
  }
  
  .header {
    background-color: #e64626; /* Orange header background */
    color: #fff; /* White text color */
    padding: 10px;
    margin-bottom: 20px;
  }
  
  .content {
    max-width: 1600px;
    margin-left: 100px;
  }
  
  section {
    margin-bottom: 30px;
  }
  
  h1, h2 {
    color: #333; /* Dark header text color */
  }

  h2 {
    font-size: 1.5em;
  }

  p, ul {
    font-size: 1.2em;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  ul li::before {
    content: '\2022'; /* Bullet character */
    color: #e64626; /* Orange bullet color */
    font-weight: bold;
    display: inline-block;
    width: 1em;
    margin-left: -1em;
  }
  /* Add styles for icons */
  .i {
    margin-right: 8px; /* Adjust spacing between icon and text */
    font-size: 1.2em;
  }

  /* Blinking animation */
  @keyframes blink {
    0%, 100% { color: black; }
    50% { color: #e64626; } /* Orange color */
  }
  .colorOrange{
    color: #e64626; /* Orange bullet color */
  }
  .quick-start-guide {
    animation: blink 1s infinite;
  }

  </style>
  
  <script>
    export default {
      mounted() {
        // Use $nextTick to ensure the DOM has been updated
        this.$nextTick(() => {
          // Stop blinking after 5 seconds
          setTimeout(() => {
            const blinkElement = document.querySelector('.blink');
            if (blinkElement) {
              blinkElement.style.animation = 'none';
            }
          }, 1000);
        });
      },
    };
  </script>
  