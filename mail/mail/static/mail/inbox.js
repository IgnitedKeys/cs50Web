document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('form').onsubmit = send_email;
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  //send email
  
}

function send_email(event) {
  event.preventDefault;

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  if (recipients.length == 0) return;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    
  });
  localStorage.clear();

  //REDIRECT TO SENT MAILBOX
  load_mailbox('sent');
  return false;
}

function view_email(id) {
  


  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#single-email').style.display = 'block';

      document.querySelector('#single-email').innerHTML = ` 
        <ul class="list-group>
          <li class="list-group-item>From:${email.sender}</li>
          <li class="list-group-item>To:${email.recipients}</li>
          <li class="list-group-item>Subject:${email.subject}</li>
          <li class="list-group-item>Timestamp:${email.timestamp}</li>
          <li class="list-group-item>${email.body}</li>
          
          <li class="list-group-item>${email.archived}</li>
        </ul>
      `
      //read
      if(!email.read){
        fetch(`/emails/${email.id}`,{
          method: 'PUT',
          read: true
        })
      }

      //archive
      const button = document.createElement('button');
      button.innerHTML = !email.archived ? "unarchive" : "archived";
      button.className = !email.archived ? "btn btn-secondary" : "btn btn-primary";
      button.addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
          
        })
        .then(() => {load_mailbox('archive')});
    });

      document.querySelector('#single-email').append(button);

      //reply
      const reply_button = document.createElement('button');
      reply_button.innerHTML = "Reply";
      reply_button.className = "btn btn-secondary";

      reply_button.addEventListener('click', () => {
        compose_email();

        let subject = email.subject;
        if(subject.split(' ',1)[0] != "Re:"){
          subject = "Re: " + email.subject;
        }

        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: ${email.body}`;
        
      });
      document.querySelector('#single-email').append(reply_button);

    });
    

}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);

    emails.forEach(email => {
      const newEmail = document.createElement('div');
      newEmail.className = "list-group-item";
      newEmail.innerHTML = `
      <h3>Sender: ${email.sender} Recipient: ${email.recipients}</h3>
      <h3>Subject: ${email.subject}</h3>
      <p>${email.timestamp}</p>`
      ;
      //change read/unread color
      newEmail.className = email.read ? 'email-read' : 'email-unread';


      //click to email
      newEmail.addEventListener('click', ()=> view_email(email.id));
      document.querySelector('#emails-view').append(newEmail);
    });
    
  }).catch(error => {
    console.log("Error:", error);
  });
}
 

