# Kosaka Calamity (c) Ascellayn (2025) - TSN License 1.0 - Base
from TSN_Abstracter import *;
import flask, json;

Calamity_Version: str = "v1.0";
Root_CFG: dict = File.JSON_Read("Root_CFG.json");
Debug_Mode: bool = Root_CFG["Debug"];
Root_CFG["Version"] = Calamity_Version;

Tokens: dict = File.JSON_Read("Kosaka_Tokens.json");



def Verify_Token(Token: str) -> bool | str:
	for Bot in Tokens:
		if (Tokens[Bot] == Token): return True, Bot;
	return Root_CFG["Allow_Anonymous"], "Anonymous";

def Blacklist_Manager(AddRequest: bool, Type: str, ID: int, Identity: tuple[bool, str]) -> dict:
	Log.Info(f"{Identity[1]} asked us to {'Blacklist' if (AddRequest) else 'Pardon'} {Type} of ID {ID}.");
	Blacklist: dict = File.JSON_Read("Blacklist.json");

	doUpdate: bool = False;
	if (Type not in Blacklist.keys()):
		Blacklist[Type] = []; doUpdate = True;

	Message: str = "";
	if (AddRequest):
		if (ID in Blacklist[Type]): Message = f"Authenticated as {Identity[1]}, {Type} ID {ID} was already added to the Blacklist.";
		else: Blacklist[Type].append(ID); doUpdate = True; Message = f"Authenticated as {Identity[1]}, added the {Type} ID {ID} to the Blacklist.";
	else:
		if (ID in Blacklist[Type]): doUpdate = True; Blacklist[Type].remove(ID); Message = f"Authenticated as {Identity[1]}, removed {Type} ID {ID} from the Blacklist.";
		else: Blacklist[Type].append(ID); Message = f"Authenticated as {Identity[1]}, {Type} ID {ID} was not in the Blacklist already.";

	if (doUpdate): File.JSON_Write("Blacklist.json", Blacklist);

	return {
		"Updated": doUpdate,
		"Message": Message
	};



API = flask.Flask(__name__);
# GET Routes
@API.route("/", methods=["GET"])
def Root() -> None: return Root_CFG;
@API.route("/blacklist", methods=["GET"])
def Blacklist() -> None: return File.JSON_Read("Blacklist.json");



# POST Routes
@API.route("/remove", methods=["POST"])
def Remove() -> None:
	Log.Info(f"Received Blacklist Remove Request from {flask.request.host}...");
	try:
		Request: dict = json.loads(flask.request.get_json());
		Token: str = Request.get("Token", "Anonymous");
		ID: int = Request["ID"];
		Type: str = Request["Type"];
	except Exception as Except:
		Log.Fetch_ALog().EXCEPTION(Except)
		flask.abort(400);

	Identity: tuple = Verify_Token(Token);
	if (not Identity[0]): flask.abort(403);

	return Blacklist_Manager(False, Type, ID, Identity);



@API.route("/add", methods=["POST"])
def Add() -> None:
	Log.Info(f"Received Blacklist Add Request from {flask.request.host}...");
	try:
		Request: dict = json.loads(flask.request.get_json());
		Token: str = Request.get("Token", "Anonymous");
		ID: int = Request["ID"];
		Type: str = Request["Type"];
	except Exception as Except:
		Log.Fetch_ALog().EXCEPTION(Except)
		flask.abort(400);

	Identity: tuple = Verify_Token(Token);
	if (not Identity[0]): flask.abort(403);

	return Blacklist_Manager(True, Type, ID, Identity);





if (__name__ == '__main__'):
	Log.Clear(); TSN_Abstracter.Require_Version((3,0,0));
	Config.Logger.Print_Level = 15 if (Debug_Mode) else 20;
	Config.Logger.File = True;
	
	Log.Stateless(f"Kosaka Blacklist Synchronization Server (Calamity) {Calamity_Version}");

	API.run(Root_CFG["WebServer"]["Host"], Root_CFG["WebServer"]["Port"], Debug_Mode, use_reloader=False);
