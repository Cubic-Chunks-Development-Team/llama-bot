# The Llama-Bot
The Llama-Bot is a bot developed and designed by the Cubic Chunks Development Team. Unlike most bots, ours is open-source, which lets you customize it all you want to name the bot to how the bot will function.

### Small Warning
You will need to have Python installed with pip and discord.py before getting the bot onto your server!

## Getting Started
Since this bot is open-source, getting it onto your Discord server will be a bit different than normal. The following information will help you with almost the whole setup process for this bot.

### Making a Discord App & Bot
First off, you're going to need to create an app, which you can do [here](https://discordapp.com/developers/applications/me). Once you create that app, you're going to want to make a bot user within that app.

### Getting the bot to join your server
After creating your app, you're going to want to the link below:
    https://discordapp.com/oauth2/authorize?client_id=<CLIENT_ID>&scope=bot
Once there, replace the <CLIENT_ID> with the Client ID from your app. Upon opening that page, it will ask you which server you want to put the bot into, and select your desired server. You're still not quite done, though! Now, you're going to want to go to token.txt, and paste in your bot token, which you can also find in the app page. Even after all of this, there's still a bit of work to do. Because Llama-Bot is a moderation bot, you're going to have a few channels/roles that will be used to make sure the player is punished for spam.
TIMEOUT_ROLE_ID: "ROLE_ID"
    Role to use for spam-prevention role.
    
    TIMEOUT_CHANNEL_ID: "CHANNEL_ID"
    Channel to use for redirection of spammers.

    HEAVY_TIMEOUT_ROLE_ID: "ROLE_ID"
    If the role fails, secondary role will mute spammers.

    SERVER_ID: "SERVER_ID"
    Server ID for the bot.

### Launching the bot
All you need to do now is open up the bot.py provided in the file you downloaded. The bot will be on your server in no time ready to send some kiddos to the timeout corner!
