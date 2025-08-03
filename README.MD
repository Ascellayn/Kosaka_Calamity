# Kosaka Blacklist Synchronization Server
This is a very minimal Flask-Based API in which Kosaka Stable/Testing/Experimental pulls a JSON containing all the Banned Users and Servers from using Kosaka.  
This server is also known internally within TSN as "Kosaka_Calamity", a reference to the "Fox of Calamity" which... Is Kosaka. If you know about BA, you know exactly what I'm referring to.  


## Usage
### Calamity Setup
**This isn't really something you can use as it is purposefully built for the conditions Kosaka is in. As Kosaka is split into 3 different versions, all of which are as of right now currently closed source and unavailable, you may find this quite useless unless you use this for your own bot projects I guess?**
- Specify "Tokens" in your `Kosaka_Tokens.json" for each Kosaka Instance such as:
```json
{
	"Kosaka_Stable": "MyStablePassword",
	"Kosaka_Testing": "MyTestingPassword",
	"Kosaka_Experimental": "MyExperimentalPassword"
}
```
*These tokens can be anything, they're just a simple check which is honestly useless as Calamity should NEVER be exposed to the public internet.*  
You may specify only one token for all your bots, however obviously this would reduce security (... but once again this should be fine honestly).  
This behavior of checking for identity can be disabled in the `Root_CFG.json` File by editing the value of `Allow_Anonymous`.
- Run `Calamity.py`.
### Kosaka Setup
- The Calamity Server has the following routes, all of them returns JSON files.
```
[/] GET → Returns Calamity's Root_CFG.json
[/add] POST → Adds a new ID to the Blacklist
[/remove] POST → Removes an new ID from the Blacklist
```
**POST REQUEST JSON FORMAT**
```JSON
{
	"Token": "MyStablePassword",
	"ID": 311057290562371586,
	"Type:" "User" # Type can be virtually anything, Calamity does not do any checks here.
}
```
**[/add] OR [/remove] RETURN JSON EXAMPLE**
```JSON
{
	"Updated": true,
	"Message": "Authenticated as Kosaka_Stable, added the User ID 311057290562371586 to the Blacklist."
}
```

## Dependencies
- [TSN Abstracter v3.0.0 (or above)](https://github.com/Ascellayn/TSN_Abstracter)
- python3-flask