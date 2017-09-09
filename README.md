# The Llama-Bot
The Llama-Bot is a bot developed and designed by the Cubic Chunks Development Team. Unlike most bots, ours is open-source, which lets you customize it all you want to name the bot to how the bot will function.

### Small Warning
You will need to have Python installed with Pip and discord.py before getting the bot onto your server!

## What can this bot do?
This bot is still being coded, and many features are still being planned, but I can tell you about 2 things. Both of them are still in development, but atleast one of them is stable.

### Anti-Spam System
#### What does this do?
Like the name implies, it will detect spam, and send players to a channel for a certain amount of time before being let out. If this fails, there is a backup role that you can give them to completely mute the player.
#### How does it do it?
Every time a player sends a chat message, they "heat up" by a certain amount, and when they are not sending messages, they cool down. When their heat reaches a certain threshold then the spam detection will be triggered

### Quoting System
#### What does this do?
It keeps a bunch of quotes in a file for you to retrieve later. You will be able to add and remove quotes via the chat.
#### How does it do it?
This is still in development, so we're still pondering how it will keep them in storage, but it will once it's done.

## Getting Started
Since this bot is open-source, getting it onto your Discord server will be a bit different than normal. The following information will help you with almost the whole setup process for this bot.

### Making a Discord App & Bot
First off, you're going to need to create an app, which you can do [here](https://discordapp.com/developers/applications/me). Once you create that app, you're going to want to make a bot user within that app.

### Getting the bot to join your server
After creating your app, you're going to want to the link below:

    https://discordapp.com/oauth2/authorize?client_id=<CLIENT_ID>&scope=bot
    
Once there, replace the <CLIENT_ID> with the Client ID from your app. Upon opening that page, it will ask you which server you want to put the bot into, and select your desired server. You're still not quite done, though! Now, you're going to want to go to token.txt, and paste in your bot token, which you can also find in the app page. Even after all of this, there's still a bit of work to do. Because Llama-Bot is a moderation bot, you're going to have a few channels/roles that will be used to make sure the player is punished for spam. The following below is what you'll see in your config.txt.

    # Role to use for spam-prevention role.
    TIMEOUT_ROLE_ID = 000000000000000000

    # Channel to use for redirection of spammers.
    TIMEOUT_CHANNEL_ID = 000000000000000000

    # If the role fails, secondary role will mute spammers.
    HEAVY_TIMEOUT_ROLE_ID = 000000000000000000

    # Role that will bypass spam-prevention actions.
    TIMEOUT_BYPASS_ROLE_ID = 000000000000000000

    # Server ID for the bot.
    SERVER_ID = 000000000000000000

There are more options further below in the config, but you can learn about how to use those in our config. (Still to be made.) Now all you need to do is start the bot.

### Launching the bot
All you need to do now is open up the bot.py provided in the file you downloaded. The bot will be on your server in no time ready to send some kiddos to the timeout corner!
