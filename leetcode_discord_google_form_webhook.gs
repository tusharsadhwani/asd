const PROBLEM_TITLE = 'number-of-islands';  // leetcode problem slug

const webhook = "https://discord.com/api/webhooks/.../..."

function myFunction() {
  const form = FormApp.getActiveForm();
  const allResponses = form.getResponses();
  const latestResponse = allResponses[allResponses.length - 1];
  const response = latestResponse.getItemResponses();
  const username = response[0].getResponse();

  const query = `
    query getUserData($username: String!) {
      recentSubmissionList(username: $username) {
        title
        titleSlug
        timestamp
        statusDisplay
      }
    }
  `
  const leetcodeRequest = UrlFetchApp.fetch(
    'https://leetcode.com/graphql',
    {
      "method": "post",
      "headers": { "Content-Type": "application/json" },
      muteHttpExceptions: true,
      "payload": JSON.stringify({ query, variables: { username } }),
    }
  )
  const leetcodeResponse = JSON.parse(leetcodeRequest.getContentText())
  if ('errors' in leetcodeResponse) {
    incorrectSubmission(username, "Invalid username")
    return
  }

  let filteredResponses = leetcodeResponse.data.recentSubmissionList
    .filter(el => el.titleSlug === PROBLEM_TITLE)
  
  if (filteredResponses.length == 0) {
    incorrectSubmission(username, `Submission for '${PROBLEM_TITLE}' not found on your username.`);
    return
  }

  // Filtering for latest 24 hours
  filteredResponses = filteredResponses
    .filter(el => Date.now() - el.timestamp * 1000 < 1000 * 60 * 60 * 24);

  if (filteredResponses.length == 0) {
    incorrectSubmission(username, `Submission for '${PROBLEM_TITLE}' not found in last 24 hours.`);
    return
  }

  filteredResponses = filteredResponses
    .filter(el => el.statusDisplay == 'Accepted');

  if (filteredResponses.length == 0) {
    incorrectSubmission(username `Successful submission for '${PROBLEM_TITLE}' not found.`);
    return
  }

  correctSubmission(username);
}

function incorrectSubmission(username, message) {
  UrlFetchApp.fetch(webhook,
    {
      "method": "post",
      "headers": { "Content-Type": "application/json" },
      muteHttpExceptions: true,
      "payload": JSON.stringify({
        embeds: [{
          title: `${username}: ${message}`,
          color: parseInt('#AA0000'.slice(1), 16),
          timestamp: new Date().toISOString()
        }]
      }),
    }
  );
}

function correctSubmission(username) {
  UrlFetchApp.fetch(webhook,
    {
      "method": "post",
      "headers": { "Content-Type": "application/json" },
      muteHttpExceptions: true,
      "payload": JSON.stringify({
        embeds: [{
          title: `${username}: submission successful!`,
          color: parseInt('#00FF00'.slice(1), 16),
          timestamp: new Date().toISOString()
        }]
      }),
    }
  );
}
