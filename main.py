import json
from valclient.client import Client
print('by : https://github.com/Imu-D-sama')
print('ver 0.4')
valid = False
agents = {}
seenMatches = []

with open('data.json', 'r') as f:
    data = json.load(f)
    ranBefore = data['ran']
    agents = data['agents']
    region = data['region']
    
if (ranBefore == False):
    region = input("Enter your region: ").lower()
    client = Client(region=region)
    client.activate()

    with open('data.json', 'w') as f:
            data['ran'] = True
            data['region'] = region
            json.dump(data, f, indent=4)
else:
    client = Client(region=region)
    client.activate()

while valid == False:
            try:
                preferredAgent = input(f"Preferred Agent or type dodge or ally: ").lower()
                if (preferredAgent in agents.keys() or preferredAgent == "dodge" or preferredAgent == "ally"):
                    valid = True    
                else:
                    print("Invalid Agent or Word")
            except Exception as e:
                print("Input Error")          
print("Waiting for Agent Select Screen")

while True:
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        if((preferredAgent == "dodge") and (sessionState == "PREGAME") and (client.pregame_fetch_match()['ID'] not in seenMatches)):
            print('Agent Select Screen Found')
            seenMatches.append(client.pregame_fetch_match()['ID'])
            client.pregame_quit_match()
            print('Successfully dodged the Match')
        elif((preferredAgent == "ally") and (sessionState == "PREGAME") and (client.pregame_fetch_match()['ID'] not in seenMatches)):
            print('Agent Select Screen Found')
            seenMatches.append(client.pregame_fetch_match()['ID'])
            ally = client.pregame_fetch_match()['AllyTeam']
            ally_team = ally['TeamID']
            ally_result = "Null"
            if (ally_team == 'Red'):
                ally_result = 'Attacker'
            elif (ally_team == 'Blue'):
                ally_result = 'Defender'
            print('you are:', ally_result)
        elif ((sessionState == "PREGAME") and (client.pregame_fetch_match()['ID'] not in seenMatches) and (preferredAgent in agents.keys())):
            print('Agent Select Screen Found')
            client.pregame_select_character(agents[preferredAgent])
            client.pregame_lock_character(agents[preferredAgent])
            seenMatches.append(client.pregame_fetch_match()['ID'])
            ally = client.pregame_fetch_match()['AllyTeam']
            ally_team = ally['TeamID']
            ally_result = "Null"
            if (ally_team == 'Red'):
                ally_result = 'Attacker'
            elif (ally_team == 'Blue'):
                ally_result = 'Defender'
            print('you are:', ally_result)
            print('Successfully Locked ' + preferredAgent.capitalize())
    except Exception as e:
        print('', end='') 