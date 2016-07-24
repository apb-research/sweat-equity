# sweat-equity
this contains files for the research project on sweat equity

Steps for creating ssh keys


Open Terminal.

Paste the text below, substituting in your GitHub email address.

ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Creates a new ssh key, using the provided email as a label

When you're prompted to "Enter a file in which to save the key," press Enter. This accepts the default file location.

Enter a file in which to save the key (/Users/you/.ssh/id_rsa): [Press enter]
At the prompt, type a secure passphrase. For more information, see "Working with SSH key passphrases".

Enter passphrase (empty for no passphrase): [Type a passphrase]
Enter same passphrase again: [Type passphrase again]


Adding your SSH key to the ssh-agent

Before adding a new SSH key to the ssh-agent, you should have checked for existing SSH keys and generated a new SSH key.

Ensure ssh-agent is enabled:

# start the ssh-agent in the background
eval "$(ssh-agent -s)"
Agent pid 59566
Add your SSH key to the ssh-agent. If you used an existing SSH key rather than generating a new SSH key, you'll need to replace id_rsa in the command with the name of your existing private key file.

$ ssh-add ~/.ssh/id_rsa
Add the SSH key to your GitHub account.

send the key to me using 
pbcopy < ~/.ssh/id_rsa.pub

paste in an email and I can add the key 


